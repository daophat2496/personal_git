import dags.postgres_to_bigquery.query.query_component as QueryComponent
import dags.postgres_to_bigquery.data.pg_special_type_cast as SpecialTypeCast

def query_builder(_table_name, _schema, _max_ts, _limit) :
    select_list = []

    field_format = "\"{}\""
    timestamp_field_format = "\"{}\" + INTERVAL '7 hours' AS \"{}\""
    special_field_format = "CAST(\"{}\" AS {}) AS \"{}\""

    limit = 100
    for column in _schema :
        if column["type"] == "timestamp without time zone" :
            select_list.append(timestamp_field_format.format(column["name"], column["name"]))
        elif column["type"] in SpecialTypeCast.type_cast :
            select_list.append(special_field_format.format(column["name"], SpecialTypeCast.type_cast[column["type"]], column["name"]))
        else :
            select_list.append(field_format.format(column["name"]))

    if _max_ts == None :
        where_clause = ""
    else :
        where_clause = QueryComponent.WHERE_CLAUSE.format(
            " AND COALESCE(\"LastModificationTime\" + INTERVAL '7 hours', \"CreationTime\" + INTERVAL '7 hours') > TIMESTAMP '{}'".format(_max_ts)
        )
    
    if _limit == None :
        limit_clause = ""
    else : 
        limit_clause = QueryComponent.LIMIT_CLAUSE.format(_limit)

    query = QueryComponent.SELECT_CLAUSE.format(", ".join(select_list)) \
        + QueryComponent.FROM_CLAUSE.format("\"{}\"".format(_table_name)) \
        + where_clause \
        + QueryComponent.ORDER_CLAUSE.format("COALESCE(\"LastModificationTime\", \"CreationTime\")", "ASC") \
        + limit_clause \
        + " ;"

    return query