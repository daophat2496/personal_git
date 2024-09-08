import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.bigquery import WriteToBigQuery
from apache_beam.io import ReadFromText
from apache_beam.io.jdbc import ReadFromJdbc
import typing
from apache_beam import Row

# Define pipeline options, such as runner, project, etc.
options = PipelineOptions(
    runner='DataflowRunner',
    project='',
    region='',
    temp_location='gs:// /',
    job_name='postgres-to-bigquery',
    save_main_session=True

)

# Set up PostgreSQL connection parameters
jdbc_url = 'jdbc:postgresql://:/'
table_name = ''
username = ''
password = ''

# Define the pipeline
with beam.Pipeline(options=options) as p:
    # Read data from PostgreSQL

    rows = p | 'ReadFromPostgreSQL' >> ReadFromJdbc(
        jdbc_url=jdbc_url,
        table_name=table_name,
        # query = "SELECT user_id, to_char(join_date, 'YYYY-MM-DD') as join_date, favorite_brand from users",
        driver_class_name='org.postgresql.Driver',
        username=username,
        password=password
    )

    # Optionally, apply transformations here

    schema = {
        'fields': [
            {'name': 'user_id', 'type': 'INT', 'mode': 'NULLABLE'}
            # , {'name': 'join_date', 'type': 'STRING', 'mode': 'NULLABLE'}
            , {'name': 'favorite_brand', 'type': 'STRING', 'mode': 'NULLABLE'}
        ]
    }

    # Write data to BigQuery
    rows | 'WriteToBigQuery' >> WriteToBigQuery(
        'testing.test_dataflow',
        schema=schema,
        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
    )