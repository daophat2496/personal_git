type_map = {
    "bigint": "INT64"
    , "varchar": "STRING"
    , "longtext": "STRING"
    , "datetime": "TIMESTAMP"
    , "int": "INT64"
    , "tinyint": "INT64"
    , "decimal": "FLOAT64"
    , "double": "FLOAT64"
    , "blob": "STRING"
    , "text": "STRING"
    , "float": "FLOAT64"
    , "timestamp": "TIMESTAMP"
    , "tinytext": "STRING"
    , "time": "STRING"
    , "date": "DATE" # Cast in select
    , "smallint": "SMALLINT"
    , "char": "STRING"
}

def bq_field_builder(_name, _type, _nullable) :
    fname = _name
    ftype = ""
    fmode = "NULLABLE"
    if _type in type_map:
        ftype = type_map[_type]
    else:
        ftype = "STRING"

    return {"name": fname, "type": ftype, "mode": fmode}

def ms_field_builder(_name, _type, _nullable) :
    return {"name": _name, "type": _type, "nullable": _nullable}
        
