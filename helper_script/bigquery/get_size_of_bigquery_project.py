from google.cloud import bigquery
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Path/to/credential.json"
client = bigquery.Client()

datasets = list(client.list_datasets())
total_rows = total_size_in_bytes = 0

for dataset in datasets:
    tables = client.list_tables(dataset.dataset_id)
    for table in tables:
        table_ref = client.get_table(table)
        total_rows += table_ref.num_rows
        total_size_in_bytes += table_ref.num_bytes

print(f'Total rows in project: {total_rows} rows')
print(f'Total size in project: {total_rows} bytes')