{% macro get_columns_in_relation_by_prefix(_relation, _prefix = "") %}
    {% if _prefix | length == 0 %}
        {{ return(adapter.get_columns_in_relation(_relation)) }}
    {% endif %}

    {%- set result = [] -%}
    {%- set prefix_length = _prefix | length -%}

    {% for column in adapter.get_columns_in_relation(_relation) %}
        {% if column.name[:prefix_length] == _prefix %}
            {{ result.append(column) }}
        {% endif %}
    {% endfor %}

    {{ return(result) }}
{% endmacro %}

----

{% macro get_select_as_field_string(_columns, _remove_prefix = "", _table_alias = "") %}
    {%- set column_name_list = _columns | map(attribute = 'name') -%}
    {%- set result_list = [] -%}
    {%- set return_str = "" -%}

    {% for column_name in column_name_list %}
        {{ log('HERE: ' ~ column_name) }}
        {% if column_name.startswith(_remove_prefix) %}
            {{ result_list.append(get_table_alias_string_helper(_table_alias) ~ column_name ~ ' AS ' ~ column_name[_remove_prefix | length :]) }}
        {% else %}
            {{ result_list.append(get_table_alias_string_helper(_table_alias) ~ column_name ~ ' AS ' ~ column_name) }}
        {% endif %}
    {% endfor %}

    {{ return(result_list | join(', ')) }}
{% endmacro %}

----

{% macro get_select_field_string(_columns, _remove_prefix = "", _table_alias = "") %}
    {%- set column_name_list = _columns | map(attribute = 'name') -%}
    {%- set result_list = [] -%}
    {%- set return_str = "" -%}

    {% for column_name in column_name_list %}
        {{ log('HERE: ' ~ column_name) }}
        {% if column_name.startswith(_remove_prefix) %}
            {{ result_list.append(get_table_alias_string_helper(_table_alias) ~ column_name[_remove_prefix | length :]) }}
        {% else %}
            {{ result_list.append(get_table_alias_string_helper(_table_alias) ~ column_name) }}
        {% endif %}
    {% endfor %}

    {{ return(result_list | join(', ')) }}
{% endmacro %}

----

{% macro get_where_unique_properties_query_string(_source_table_alias = "", _join_table_alias = "") %}
    {%- set result_list = [] -%}

    {% for prop in var('unique_properties') %}
        {{ result_list.append(" AND " ~ get_table_alias_string_helper(_source_table_alias) ~ prop ~ " = " ~ get_table_alias_string_helper(_join_table_alias) ~ prop) }}
    {% endfor %}

    {{ return(result_list | join(" "))}}
{% endmacro %}

----

{% macro filter_user_properties_column(_columns, _prefix = "") %}
    {%- set result = [] -%}

    {% for column in _columns %}
        {% if column["name"][_prefix | length :] in var('user_properties') %}
            {{ result.append(column) }}
        {% endif %}
    {% endfor %}

    {{ return(result) }}
{% endmacro %}

----

{% macro get_select_as_unique_properties_field(_soruce_table_alias = "", _as_prefix = "") %}
    {%- set result_list = [] -%}

    {% for unique_prop in var('unique_properties') %}
        {{ result_list.append(get_table_alias_string_helper(_soruce_table_alias) ~ unique_prop ~ " AS " ~ _as_prefix ~ unique_prop) }}
    {% endfor %}

    {{ return(result_list | join(", ")) }}

{% endmacro %}

----

{% macro get_pivot_column_in_statement(_prop_list = []) %}
    {{ return("'" ~ _prop_list | join("', '") ~ "'") }}
{% endmacro %}

----

{% macro get_unpivot_column_in_statement(_prop_list = []) %}
    {{ return (_prop_list | join (", ")) }}
{% endmacro %}