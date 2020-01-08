from flask import abort
from database import Database


def get_all_valid_tables():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table'"
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No tables found")


def get_all_valid_columns():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table_column'"
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No columns found")


def get_valid_table_by_prop_id(prop_id):
    db = Database()
    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table' 
                    AND prop->>'id' = '{prop_id}'"""
    print(statement)
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Table with prop id {prop_id} not found")


def get_valid_column_by_prop_id(prop_id):
    db = Database()
    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table_column' 
                    AND prop->>'id' = '{prop_id}'"""
    print(statement)
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Column with prop id {prop_id} not found")


def search_valid_tables_by_schema(schema_name):
    db = Database()
    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table' 
                    AND prop->>'schema_name' ILIKE '{schema_name}'"""
    print(statement)
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Table with schema name {schema_name} not found")


def search_valid_columns_by_schema(schema_name):
    db = Database()
    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table_column' 
                    AND prop->>'schema_name' ILIKE '{schema_name}'"""
    print(statement)
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Column with schema name {schema_name} not found")
