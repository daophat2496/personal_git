import os 
from datetime import datetime
from datetime import timedelta
import json
import requests
import time

import os.path
from os import path

from airflow import models 
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

current_dir = os.path.dirname(__file__)
home_path='/tmp'
prefix = 'des_prefix_'
yesterday_date_string = (datetime.now() - timedelta(days = 1)).strftime('%Y%m%d')
two_day_ago_date_string_formatted = (datetime.now() - timedelta(days = 2)).strftime('%Y-%m-%d')
one_day_ago_date_string_formatted = (datetime.now() - timedelta(days = 1)).strftime('%Y-%m-%d')
export_file_name = 'branchio_install_event_export_' + yesterday_date_string + '.json'
export_file_name_full_path = "{}/{}".format(home_path, export_file_name)

# List demand fields to export. Docs: https://help.branch.io/developers-hub/reference/custom-exports-api
export_fields = [
    "event_timestamp"
    , "id"
    , "name"
    , "last_attributed_touch_data_custom_fields"
    , "last_attributed_touch_data_tilde_feature"
    , "last_attributed_touch_data_tilde_channel"
    , "last_attributed_touch_data_tilde_campaign"
]

GCS_BUCKET = ""
BQ_PROJECT_ID = ""
BQ_DATASET_NAME = ""
BQ_TABLE_NAME = ""

# Replace app_id
url = "https://api2.branch.io/v2/logs?app_id=<>"
payload = {
    "report_type": "eo_install",
    "fields": export_fields,
    "limit": 50000,
    "timezone": "UTC",
    "response_format": "json",
    "start_date": two_day_ago_date_string_formatted + "T17:00:00Z",
    "end_date": one_day_ago_date_string_formatted + "T16:59:59Z"
}

with open("{}/schemas/branchio_install_event.json".format(current_dir)) as f:
    bq_schema = json.load(f)

def trigger_export_branchio() :
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Access-Token": ""
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200 :
        response_json = response.json()
        return response.status_code, response_json["handle"], response_json["export_job_status_url"]
    
    print("trigger_export_branchio " + str(response.status_code))
    return response.status_code, None, None

def check_branchio_job_status(_export_job_status_url) :
    headers = {
        "Accept": "application/json",
        "Access-Token": ""
    }
    response = requests.get(_export_job_status_url, headers=headers)

    if response.status_code == 200 :
        response_json = response.json()
        if response_json["status"] == "complete" :
            return response.status_code, response_json["status"], response_json["response_url"]
        print("check_branchio_job_status " + str(response.status_code))
        return response.status_code,  response_json["status"], None
    print("check_branchio_job_status " + str(response.status_code))
    return response.status_code, None, None

def export_from_branchio() :
    tr_status_code, handle_id, job_status_url = trigger_export_branchio()
    if tr_status_code != 200 :
        print("trigger export failed " + str(tr_status_code))
        return "failed"
    
    job_response_status, job_status, export_url = check_branchio_job_status(job_status_url)
    while 1 == 1 :
        if job_response_status != 200 or (job_response_status == 200 and job_status == "fail") :
            print("check job status failed " + str(job_response_status))
            return "failed"
        if job_status == "pending" or job_status == "running" :
            time.sleep(60)
            job_response_status, job_status, export_url = check_branchio_job_status(job_status_url)
            print("the job has not done " + str(job_response_status))
            continue
        elif job_status == "complete" :
            break
        else :
            print("Cannot check job status " + str(job_response_status))
            return "failed"
    
    r = requests.get(export_url, allow_redirects=True)

    with open("{}".format(export_file_name_full_path), 'wb') as f:
        f.write(r.content)
    
    print("success " + export_file_name)
    # print(path.exists("{}".format(export_file_name_full_path)))
    # print(os.getcwd())
    # print(os.listdir())
    return export_file_name

with models.DAG(
    dag_id = prefix + 'branchio_to_bigquery'
    , schedule_interval = '1 3 * * *'
    , tags = ['branch io']
    , start_date = datetime(2022, 7, 8)
    , catchup = False
) as dag:

    create_local_file = BashOperator(
        task_id = 'create_file_to_store'
        # , bash_command = 'touch {} | chmod 777 {}'.format(export_file_name_full_path, export_file_name_full_path)
        , bash_command = 'touch {}'.format(export_file_name_full_path)
    )

    export_branchio_data = PythonOperator(
        task_id = 'export_branchio_data_to_json'
        , python_callable = export_from_branchio
    )

    local_to_gcs = LocalFilesystemToGCSOperator(
            task_id = prefix + 'upload_branchio_export_to_gcs'
            , gcp_conn_id = ''
            , bucket = GCS_BUCKET
            , src = export_file_name_full_path
            , dst = export_file_name
            , gzip = False
            , default_args = {
                "trigger_rule": "all_done"
            }
        )
    
    gcs_to_bigquery = GCSToBigQueryOperator(
            task_id = prefix + 'branchio_gcs_to_bigquery'
            , gcp_conn_id = ''
            , bucket = GCS_BUCKET
            , source_objects = [export_file_name]
            , destination_project_dataset_table = "{}.{}.{}".format(BQ_PROJECT_ID, BQ_DATASET_NAME, BQ_TABLE_NAME)
            , autodetect = True 
            , create_disposition = 'CREATE_IF_NEEDED'
            , write_disposition = 'WRITE_APPEND'
            , source_format = 'NEWLINE_DELIMITED_JSON'
            , schema_update_options = ['ALLOW_FIELD_ADDITION']
            , schema_fields = bq_schema
        )
    
    create_local_file >> export_branchio_data >> local_to_gcs >> gcs_to_bigquery
