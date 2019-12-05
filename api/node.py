from collections import Sequence
from datetime import datetime
import json
from flask import make_response, abort
from config import db
import psycopg2.extras
from models import Node, NodeSchema
from database import Database


def read_all():
    db = Database()
    nodes = db.execute(f"SELECT * FROM tbl_node")
    if nodes is not None:
        return nodes

    abort(404, f"Error fetching nodes")


def read_one(guid):
    db = Database()
    node = db.execute(f"SELECT * FROM tbl_node where guid = '{guid}'")
    if node is not None:
        return node, 200

    abort(404, f"Node with guid {guid} not found")


def get_by_prop_id(id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"Node with prop.id {id} not found")


def create(node):
    print(node)
    statement = "INSERT INTO tbl_node (prop_id, prop) VALUES "
    for node_item in node:
        prop = node_item.get("prop")
        prop_id = prop.get("id")
        if prop is None:
            abort(409, f"The node must have a prop key with value of type dict")
        if id is None:
            abort(409, f"The prop dict should contain id property of type string")

        json_prop = json.dumps(prop).replace("\'", "''")
        statement = statement + f"({json.dumps(prop_id)}, E'{json_prop}'), "

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    print(statement)
    node = db.execute(statement)
    return node


def update(node):
    print("put:", node)
    statement = "INSERT INTO tbl_node (prop_id, prop) VALUES "
    for node_item in node:
        prop = node_item.get("prop")
        prop_id = prop.get("id")
        if prop is None:
            abort(409, f"The node must have a prop key with value of type dict")
        elif id is None:
            abort(409, f"The prop dict should contain id property of type string")
        else:
            json_prop = json.dumps(prop).replace("\'", "''")
            statement = statement + f"({json.dumps(prop_id)}, E'{json_prop}'), "

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    # On receiving a prop_id that already exist it will instead update the prop
    statement = statement + " ON CONFLICT (prop_id) DO UPDATE SET prop = excluded.prop"
    print(statement)
    node = db.execute(statement)
    return node


def delete(prop_id):
    print("delete:", prop_id)

    # Checking if node with prop_id exist
    db = Database()
    check_statement = f"SELECT * FROM tbl_node WHERE prop_id = '{prop_id}'"
    node = db.execute(check_statement)
    if node is None:
        abort(404, f"Could not find node with prop_id = {prop_id}")
    else:
        statement = f"DELETE FROM tbl_node WHERE 'prop_id'={prop_id}  "
        db.execute(statement)
        return f"Node with prop_id = {prop_id} deleted", 200
