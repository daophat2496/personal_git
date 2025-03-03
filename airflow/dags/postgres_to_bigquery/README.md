# Postgres to BigQuery DAG

This directory contains an Apache Airflow DAG for transferring data from a PostgreSQL database to Google BigQuery.

## Overview

The DAG defined in this directory performs the following tasks:
1. Extracts data from a PostgreSQL database.
2. Transforms the data if necessary.
3. Loads the data into a Google BigQuery table.

## Files

- `postgres_to_bigquery_dag.py`: The main DAG definition file.
- `sql/`: Directory containing SQL queries used in the DAG.
- `utils/`: Directory containing utility functions and classes used in the DAG.

## Prerequisites

- Apache Airflow installed and configured.
- Access to a PostgreSQL database.
- Access to a Google BigQuery project and dataset.
- Service account key file for Google Cloud Platform with BigQuery permissions.

## Configuration

1. **Airflow Connections**:
   - Create a connection in Airflow for PostgreSQL with the following details:
     - Conn Id: `postgres_default`
     - Conn Type: `Postgres`
     - Host, Schema, Login, Password, Port: (as per your PostgreSQL configuration)
   - Create a connection in Airflow for Google Cloud with the following details:
     - Conn Id: `google_cloud_default`
     - Conn Type: `Google Cloud`
     - Keyfile Path: Path to your GCP service account key file.

2. **Airflow Variables**:
   - Set the following Airflow variables:
     - `gcp_project_id`: Your GCP project ID.
     - `gcp_dataset_id`: Your BigQuery dataset ID.
     - `postgres_table_name`: The name of the PostgreSQL table to transfer.

## Usage

1. Place the DAG file (`postgres_to_bigquery_dag.py`) in your Airflow DAGs directory.
2. Ensure the SQL queries and utility functions are in the appropriate directories (`sql/` and `utils/`).
3. Start the Airflow scheduler and webserver.
4. Trigger the DAG from the Airflow web interface.