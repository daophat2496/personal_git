import mysql.connector
import load_configurations as LoadConfigurations 
import table_list as TableList
import query.get_schema_query as Query
import json
import schema_field_builder as FieldBuilder

def main() :
    config = LoadConfigurations.loadConfigurations()

    conn = mysql.connector.connect(
        database=config['db_dbname']
        , user=config['db_username']
        , password=config['db_password']
        , host=config['db_url']
        , port=config['db_port']
    )

    cursor = conn.cursor()
    
    for table in TableList.loaded_table :
        bq_schema = []
        ms_schema = []
        cursor.execute(Query.query.format(table))

        rows = cursor.fetchall()
        for row in rows:
            bq_schema.append(FieldBuilder.bq_field_builder(row[0], row[1], row[2]))
            ms_schema.append(FieldBuilder.ms_field_builder(row[0], row[1], row[2]))
        
        with open('dest/{}.json'.format(table), 'w') as f:
            json.dump(bq_schema, f, indent=4)

        with open('dest/ms_{}.json'.format(table), 'w') as f:
            json.dump(ms_schema, f, indent=4)

if __name__ == "__main__" :
    main()