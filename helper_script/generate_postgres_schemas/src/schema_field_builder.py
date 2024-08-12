type_map = {
    "smallint" : "INT64"
    , "bigint" : "INT64"
    , "integer" : "INT64"
    , "boolean" : "BOOLEAN"
    , "timestamp without time zone" : "TIMESTAMP"
    , "timestamp": "TIMESTAMP"
    , "double precision": "FLOAT64"
    , "numeric": "FLOAT64"
    , "real": "FLOAT64"
    , "decimal": "FLOAT64"
    , "date": "DATE"
}

def bq_field_builder(_name, _type, _nullable) :
    fname = _name
    ftype = ""
    fmode = "REPEATED" if _type == "ARRAY" else "NULLABLE"
    if _type in type_map:
        ftype = type_map[_type]
    else:
        ftype = "STRING"

    return {"name": fname, "type": ftype, "mode": fmode}

def pg_field_builder(_name, _type, _nullable) :
    return {"name": _name, "type": _type, "nullable": _nullable}
        
