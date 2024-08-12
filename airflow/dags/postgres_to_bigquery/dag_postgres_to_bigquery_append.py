import os 
from datetime import datetime
import json

from airflow import models 
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import dags.postgres_to_bigquery.data.table_list_append as TableList
import dags.postgres_to_bigquery.query.export_query_append_builder as ExportQueryBuilder

BQ_PROJECT_ID = ""
BQ_DATASET_NAME = ""
GCS_BUCKET = ""
FILENAME = "some_prefix_{}.json"
# LIMIT = 100000
LIMIT = None

current_dir = os.path.dirname(__file__)
prefix = 'some_prefix_'

with models.DAG(
    dag_id = prefix + 'raw_data_postgres_to_bigquery_append_table'
    , schedule_interval = '10 */2 * * *'
    , tags = ["postgres", "append tables"]
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

        # get max timestamp
        bq_hook = BigQueryHook(
            gcp_conn_id = ""
            , use_legacy_sql = False
            , location = ""
        )

        bqmaxts = bq_hook.get_records(
            sql = "SELECT FORMAT_TIMESTAMP('%F %H:%M:%E*S', MAX(COALESCE(LastModificationTime, CreationTime)))" \
                    " FROM {}.{}.{}".format(BQ_PROJECT_ID, BQ_DATASET_NAME, table)
        )

        result_bqmaxts = bqmaxts[0][0]
        # print(result_bqmaxts)

        postgres_to_gcs = PostgresToGCSOperator(
            task_id = prefix + "postgres_to_gcs_{}".format(table)
            , postgres_conn_id = "connection_id"
            , gcp_conn_id = 'connection_id'
            , sql = ExportQueryBuilder.query_builder(table, pg_schema, _max_ts = result_bqmaxts, _limit = LIMIT)
            , bucket = GCS_BUCKET
            , filename = FILENAME.format(table)
            , gzip = False
            , default_args = {
                "trigger_rule": "all_done"
            }
        )
        postgres_to_gcs_list.append(postgres_to_gcs)

        gcs_to_bigquery = GCSToBigQueryOperator(
            task_id = prefix + "gcs_to_bigquery_{}".format(table)
            , gcp_conn_id = "connection_id"
            , bucket = GCS_BUCKET
            , source_objects = [FILENAME.format(table)]
            , destination_project_dataset_table = "{}.{}.{}".format(BQ_PROJECT_ID, BQ_DATASET_NAME, table)
            , autodetect = True 
            , create_disposition = 'CREATE_IF_NEEDED'
            , write_disposition = 'WRITE_APPEND'
            , source_format = 'NEWLINE_DELIMITED_JSON'
            , schema_fields = bq_schema
        )
        gcs_to_bigquery_list.append(gcs_to_bigquery)

    # chain(*postgres_to_gcs_list, *gcs_to_bigquery_list)
    for i in range(len(postgres_to_gcs_list)) :
        if i < len(postgres_to_gcs_list) - 1:
            postgres_to_gcs_list[i] >> [postgres_to_gcs_list[i + 1], gcs_to_bigquery_list[i]]
        
        postgres_to_gcs_list[i] >> gcs_to_bigquery_list[i]