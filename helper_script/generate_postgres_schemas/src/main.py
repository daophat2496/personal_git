import psycopg2
import load_configurations as LoadConfigurations 
import table_list as TableList
import query.get_schema_query as Query
import json
import schema_field_builder as FieldBuilder
from sshtunnel import SSHTunnelForwarder

def main() :
    config = LoadConfigurations.loadConfigurations()

    ssh_server = SSHTunnelForwarder(
        (config['ssh_host'], 22)
        , ssh_username = config['ssh_username'], ssh_private_key = config['ssh_key_path']
        , remote_bind_address=('localhost', 5432)
        , local_bind_address=('localhost', 5431)
    )
    ssh_server.start()

    conn = psycopg2.connect(
        database=config['db_dbname']
        , user=config['db_username']
        , password=config['db_password']
        , host=ssh_server.local_bind_host
        , port=ssh_server.local_bind_port
    )

    cursor = conn.cursor()
    
    for table in TableList.loaded_table :
        bq_schema = []
        pg_schema = []
        cursor.execute(Query.query.format(table))

        rows = cursor.fetchall()
        for row in rows:
            bq_schema.append(FieldBuilder.bq_field_builder(row[0], row[1], row[2]))
            pg_schema.append(FieldBuilder.pg_field_builder(row[0], row[1], row[2]))
        
        with open('dest/{}.json'.format(table), 'w') as f:
            json.dump(bq_schema, f, indent=4)

        with open('dest/pg_{}.json'.format(table), 'w') as f:
            json.dump(pg_schema, f, indent=4)

if __name__ == "__main__" :
    main()