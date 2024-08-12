{% macro get_table_alias_string_helper(_alias) %}
    {% if _alias | length == 0 %}
        {{ return("") }}
    {% endif %}
    
    {{ return(_alias ~ ".") }}
{% endmacro %}

{% macro test(_value) %}
    {% if _alias | length == 0 %}
        {{ return("") }}
    {% endif %}
    
    {{ return(_alias ~ ".") }}
{% endmacro %}


    -- _join_type: LEFT JOIN | RIGHT JOIN | ....
    -- target_type: view | other
    -- _target_table: join table name
    -- _source_table_alias
    -- _source_join_field: field name for condition
    -- _target_join_field: field name for condition
{% macro event_select_clause_builder(_join_type, _target_type, _target_table, _source_table_alias, _source_join_field, _target_join_field) %}
    {% if _target_table | length == 0 %}
        {{ return("") }}
    {% endif %}

    {% set ttype = "" %}
    {% if _target_type == "view" %}
        {% set ttype = "v_" %}
    {% endif %}

    {{ return(
        " " ~ _join_type ~ " " ~ ttype ~ _target_table ~ 
        " ON " ~ _target_table ~ "." ~ _target_join_field ~ 
        " = " ~ _source_table_alias ~ "." ~ _source_join_field
    ) }}

{% endmacro %}