import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
# from apache_beam.io import BigQueryDisposition, WriteDisposition
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.io.jdbc import ReadFromJdbc
import typing
from apache_beam import Row

class FormatAsDictFn(beam.DoFn):
    def process(self, element):
        # Assuming element is a tuple of (column1, column2)
        result = {
            'user_id': element[0]
            , 'favorite_brand': element[1]
            , 'join_date': element[2]
        }
        return [result]

def run():
    # Define pipeline options, such as runner, project, etc.
    options = PipelineOptions(
        runner='DataflowRunner'
        , project=''
        , region=''
        , temp_location='gs://phatdao/dataflow'
        , job_name=''
        # save_main_session=True
    )

    # Set up PostgreSQL connection parameters
    jdbc_url = 'jdbc:postgresql://:/'
    table_name = ''
    username = ''
    password = ''

    # Define the pipeline
    with beam.Pipeline(options=options) as p:
        # Read data from PostgreSQL

        rows = (
            p
            | "ReadFromPostgres" >> ReadFromJdbc(
                query = "SELECT user_id, favorite_brand, TO_CHAR(join_date, 'YYYY-MM-DD') FROM users"
                , driver_class_name = "org.postgresql.Driver"
                , jdbc_url = jdbc_url
                , username = username 
                , password = password 
                , table_name = table_name
            )
            | "FormatToDict" >> beam.ParDo(FormatAsDictFn())
        )

        # Optionally, apply transformations here

        # schema = {
        #     'fields': [
        #         {'name': 'user_id', 'type': 'INTEGER', 'mode': 'NULLABLE'}
        #         # , {'name': 'join_date', 'type': 'STRING', 'mode': 'NULLABLE'}
        #         , {'name': 'favorite_brand', 'type': 'STRING', 'mode': 'NULLABLE'}
        #         , {'name': 'join_date', 'type': 'DATE', 'mode': 'NULLABLE'}
        #     ]
        # }
        schema = "user_id:INTEGER,favorite_brand:STRING,join_date:DATE"

        # Write data to BigQuery
        rows | "WriteToBigQuery" >> WriteToBigQuery(
            "testing.test_dataflow"
            , schema = schema 
            , write_disposition = BigQueryDisposition.WRITE_APPEND
            , create_disposition = BigQueryDisposition.CREATE_IF_NEEDED
        )

if __name__ == '__main__':
  run()