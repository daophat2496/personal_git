import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from apache_beam.io.gcp.bigquery import BigQueryDisposition
from apache_beam.io.gcp.bigquery import WriteToBigQuery

class SimpleDataProcessing(beam.DoFn):
    def process(self, element, *args, **kwargs):
        import json 
        from datetime import datetime
        record = json.loads(element)
        record["join_ts"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        yield record

def run():
    pupsub_subscription = ""

    options = PipelineOptions(
        project=''
        , region='asia-southeast1'
        , temp_location='gs:////temp'
        , job_name='stream-pubsub-to-bigquery'
        , staging_location = 'gs:////staging'
        # save_main_session=True
    )
    options.view_as(StandardOptions).streaming = True
    options.view_as(StandardOptions).runner = 'DataflowRunner'

    schema = "user_id:INTEGER,favorite_brand:STRING,join_date:DATE,join_ts:TIMESTAMPT"

    with beam.Pipeline(options = options) as p:
        messages = p | "Read from Pubsub" >> beam.io.ReadFromPubSub(subscription = pupsub_subscription)
        
        messages | beam.Map(print)

        (
            messages
            | "Process Data" >> beam.ParDo(SimpleDataProcessing())
            | "Write to Bigquery" >> WriteToBigQuery(
                "testing.test_dataflow"
                , schema = schema
                , write_disposition = BigQueryDisposition.WRITE_APPEND
                , create_disposition = BigQueryDisposition.CREATE_IF_NEEDED
            )
        )

if __name__ == "__main__":
    run()