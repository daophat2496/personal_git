import os 
from datetime import datetime
import json

from airflow import models 
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import dags.postgres_to_bigquery.data.table_list as TableList
import dags.postgres_to_bigquery.query.export_query_builder as ExportQueryBuilder

BQ_PROJECT_ID = ""
BQ_DATASET_NAME = ""
BQ_TABLE_NAME = "{}"
GCS_BUCKET = ""
FILENAME = "some_prefix_{}.json"

current_dir = os.path.dirname(__file__)
prefix = 'some_prefix_'

with models.DAG(
    dag_id = prefix + 'raw_data_postgres_to_bigquery'
    , schedule_interval = '0 */2 * * *'
    , tags = ["postgres"]
    , start_date = datetime(2022, 7, 8)
    , catchup = False
) as dag:
    postgres_to_gcs_list = []
    gcs_to_bigquery_list = []
    
    for table in TableList.loaded_table :
        with open("{}/schemas/{}.json".format(current_dir, table)) as f:
            bq_schema = json.load(f)

        with open("{}/schemas/pg_{}.json".format(current_dir, table)) as f:
            pg_schema = json.load(f)

        print(ExportQueryBuilder.query_builder(table, bq_schema))
        postgres_to_gcs = PostgresToGCSOperator(
            task_id = prefix + 'postgres_to_gcs_{}'.format(table)
            , postgres_conn_id = 'connection_id'
            , gcp_conn_id = 'connection_id'
            , sql = ExportQueryBuilder.query_builder(table, pg_schema)
            , bucket = GCS_BUCKET
            , filename = FILENAME.format(table)
            , gzip = False
            , default_args = {
                "trigger_rule": "all_done"
            }
        )
        postgres_to_gcs_list.append(postgres_to_gcs)

        gcs_to_bigquery = GCSToBigQueryOperator(
            task_id = prefix + 'gcs_to_bigquery_{}'.format(table)
            , gcp_conn_id = 'connection_id'
            , bucket = GCS_BUCKET
            , source_objects = [FILENAME.format(table)]
            , destination_project_dataset_table = "{}.{}.{}".format(BQ_PROJECT_ID, BQ_DATASET_NAME, table)
            , autodetect = True 
            , create_disposition = 'CREATE_IF_NEEDED'
            , write_disposition = 'WRITE_TRUNCATE'
            , source_format = 'NEWLINE_DELIMITED_JSON'
            , schema_fields = bq_schema
        )
        gcs_to_bigquery_list.append(gcs_to_bigquery)

    # chain(*postgres_to_gcs_list, *gcs_to_bigquery_list)
    for i in range(len(postgres_to_gcs_list)) :
        if i < len(postgres_to_gcs_list) - 1:
            postgres_to_gcs_list[i] >> [postgres_to_gcs_list[i + 1], gcs_to_bigquery_list[i]]
        
        postgres_to_gcs_list[i] >> gcs_to_bigquery_list[i]