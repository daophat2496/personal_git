import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
# from apache_beam.io import BigQueryDisposition, WriteDisposition
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.io.jdbc import ReadFromJdbc
from google.cloud import bigquery
import typing
from apache_beam import Row

class FormatAsDictFn(beam.DoFn):
    def process(self, element):
        # Assuming element is a tuple of (column1, column2)
        result = {
            'user_id': element[0]
            , 'favorite_brand': element[1]
            , 'join_date': element[2]
            # , 'join_ts': element[3]
            , 'no_data': element[3]
        }
        return [result]

def get_table_schema(project_id, dataset_name, table_name):
    client = bigquery.Client()
    table_id = f"{project_id}.{dataset_name}.{table_name}"
    table = client.get_table(table_id)
    return table.schema

def update_table_schema(dataset_name, table_name, new_fields):
    if new_fields or len(new_fields) == 0:
        return
    
    client = bigquery.Client()
    table_id = f"{client.project}.{dataset_name}.{table_name}"
    table = client.get_table(table_id)
    original_schema = table.schema

    # Adding new fields
    updated_schema = original_schema[:]  # Create a copy of the schema
    updated_schema.extend(new_fields)  # new_fields should be a list of bigquery.SchemaField objects

    table.schema = updated_schema
    client.update_table(table, ["schema"])  # Update the table schema

def run():
    # Define pipeline options, such as runner, project, etc.
    options = PipelineOptions(
        runner='DataflowRunner'
        , project=''
        , region='asia-southeast1'
        , temp_location='gs:///'
        , job_name='postgres-to-bigquery'
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
                query = "SELECT user_id, favorite_brand, TO_CHAR(join_date, 'YYYY-MM-DD') as join_date, TO_CHAR(join_ts + INTERVAL '7 HOURS', 'YYYY-MM-DD HH:MM:SS') as join_ts, no_data FROM users"
                , driver_class_name = "org.postgresql.Driver"
                , jdbc_url = jdbc_url
                , username = username 
                , password = password 
                , table_name = table_name
            )
            | "FormatToDict" >> beam.ParDo(FormatAsDictFn())
        )

        schema = "user_id:INTEGER,favorite_brand:STRING,join_date:DATE,no_data:STRING"
        current_schema = get_table_schema("edu20-276907", "testing", "test_dataflow")
        new_fields = [(field.split(":")[0], field.split(":")[1]) for field in schema.split(",") if field.split(":")[0] not in [field.name for field in current_schema]]

        new_field_schema = [bigquery.SchemaField(field[0], field[1], "NULLABLE") for field in new_fields]

        update_table_schema("testing", "test_dataflow", new_field_schema)

        # Write data to BigQuery
        rows | "WriteToBigQuery" >> WriteToBigQuery(
            "testing.test_dataflow"
            , schema = schema
            , write_disposition = BigQueryDisposition.WRITE_APPEND
            , create_disposition = BigQueryDisposition.CREATE_IF_NEEDED
        )

if __name__ == '__main__':
  run()