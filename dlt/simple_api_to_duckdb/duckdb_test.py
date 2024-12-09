import duckdb

conn = duckdb.connect("trip_duck.duckdb")
conn.sql("set search_path=public")
conn.sql("select * from yellow_trip_resouce;").show()
conn.sql("describe yellow_trip_resouce;").show()
conn.close()