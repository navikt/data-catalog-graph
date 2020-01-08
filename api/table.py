from flask import abort
from database import Database


def get_all_valid_tables():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table'"
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes, 200

    abort(404, "No tables found")


def get_all_valid_columns():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table_column'"
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes, 200

    abort(404, "No columns found")


def get_valid_table_by_prop_id(prop_id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table' AND prop->>'id' ='{prop_id}'"
    print(statement)
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes, 200

    abort(404, f"Table with prop.id {id} not found")


def get_valid_column_by_prop_id(prop_id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'db_table_column' AND prop->>'id' ='{prop_id}'"
    print(statement)
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes, 200

    abort(404, f"Column with prop.id {id} not found")