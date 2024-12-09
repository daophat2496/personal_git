# Simple DLT Pipeline Ingest Data From API to DuckDB

## 1. Pre-requisite
```pip install -r requirements.txt```

## 2. Run the pipeline
```python pipeline.py```

## 3. Exam data in DuckDB
```
import duckdb

conn = duckdb.connect("trip_duck.duckdb")
conn.sql("set search_path=public")
conn.sql("select * from yellow_trip_resouce;").show()
conn.sql("describe yellow_trip_resouce;").show()
conn.close()
```

## 5. Details
- Data is available in ```https://storage.googleapis.com/dtc_zoomcamp_api/yellow_tripdata_2009-06.jsonl```
- This pipeline contains 3 core concepts in DLT: **Pipeline**, **Source**, **Resource**
    - **Pipeline**: the object that will trigger the process of ingestion. Pipeline receive 1 parameter of iterator that represent list of record to be ingested.
    - **Resource**: a function that return the iterator of record to be ingested, and could be used as the parameter in pipeline.
    - **Source**: a logical group of resource. Source will return a list of resource, and is usually used for ie. different endpoint in a same api...

## 5. Notes
- **Resource could be not belong to any source, resource can be defined and used directly in pipeline