# List of macros:


## column_in_relation_helper

#### get_columns_in_relation_by_prefix
Returns the columns in a relation that start with a given prefix.

#### get_select_as_field_string
Generates a select statement with aliasing for columns, optionally removing a prefix from the column names.

#### get_select_field_string
Generates a select statement for columns, optionally removing a prefix from the column names.

#### get_where_unique_properties_query_string
Generates a WHERE clause for unique properties between two tables.

#### filter_user_properties_column
Filters columns based on user properties and an optional prefix.

#### get_select_as_unique_properties_field
Generates a select statement for unique properties with aliasing.

#### get_pivot_column_in_statement
Generates a pivot column statement from a list of properties.

#### get_unpivot_column_in_statement
Generates an unpivot column statement from a list of properties.

#### get_select_all_except_field_string
Generates a select statement for all columns except specified ones, with optional table aliasing.

## query_helper

#### get_table_alias_string_helper
Returns the table alias string with a dot if the alias is not empty.

#### event_select_clause_builder
Builds a select clause for an event with join type, target type, target table, source table alias, source join field, and target join field.