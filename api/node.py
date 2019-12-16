import logging
from collections import Sequence
from datetime import datetime
import json
from flask import make_response, abort
from config import db
import psycopg2.extras
from models import Node, NodeSchema
from database import Database


def get_all():
    db = Database()
    nodes = db.execute(f"SELECT * FROM tbl_node")
    if nodes is not None:
        return nodes

    abort(404, f"Error fetching nodes")


def get_by_guid(guid):
    db = Database()
    node = db.execute(f"SELECT * FROM tbl_node WHERE guid = '{guid}'")
    if node is not None:
        return node, 200

    abort(404, f"Node with guid {guid} not found")


def get_by_id(id):
    db = Database()
    node = db.execute(f"SELECT * FROM tbl_node WHERE id = '{id}'")
    if node is not None:
        return node, 200

    abort(404, f"Node with guid {id} not found")


def get_by_prop_id(id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"Node with prop.id {id} not found")


def get_all_nodes_by_pattern(id_pattern):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop_id LIKE '{id_pattern}%' "
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200
    
    abort(404, f"No node found with prop_id matching {id_pattern}")


def get_nodes_by_list_of_ids(id_list):
    logging.warning(id_list)
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE"
    for list_item in id_list:
        node_id = list_item.get('id')
        if node_id is None:
            abort(400, f"Request body is missing ID key of type integer")
        statement = statement + f' id = {node_id} OR'

    #DELETE the last OR in statement
    statement = statement[:-2]
    print(statement)
    nodes = db.execute(statement)
    return nodes, 200


def create(node):
    print(node)
    statement = "INSERT INTO tbl_node (prop_id, prop) VALUES "
    for node_item in node:
        prop = node_item.get("prop")
        if prop is None:
            abort(409, f"The node must have a prop key with value of type dict")
        prop_id = prop.get("id")
        if prop_id is None:
            abort(409, f"The prop dict should contain id property of type string")
        else:
            json_prop = json.dumps(prop).replace("\'", "''")
            statement = statement + f"('{prop_id}', '{json_prop}'), "

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    print(statement)
    node = db.execute(statement)
    return f" Successfully created {node} rows", 200


def update(node):
    print("put:", node)
    statement = "INSERT INTO tbl_node (prop_id, prop) VALUES "
    for node_item in node:
        prop = node_item.get("prop")
        if prop is None:
            abort(409, f"The node must have a prop key with value of type dict")
        prop_id = prop.get("id")
        if prop_id is None:
            abort(409, f"The prop dict should contain id property of type string")
        else:
            json_prop = json.dumps(prop).replace("\'", "''")
            statement = statement + f"('{prop_id}', '{json_prop}'::jsonb), "

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    # On receiving a prop_id that already exist it will instead update the prop
    statement = statement + " ON CONFLICT (prop_id) DO UPDATE SET prop = tbl_node.prop || excluded.prop"
    print(statement)
    node = db.execute(statement)
    return f"Successfully updated {node} rows", 200


def delete(prop_id):
    print("delete:", prop_id)

    # Checking if node with prop_id exist
    db = Database()
    check_statement = f"SELECT * FROM tbl_node WHERE prop_id = '{prop_id}'"
    node = db.execute(check_statement)
    if node is None:
        abort(404, f"Could not find node with prop_id = '{prop_id}'")
    else:
        node_id = node.get('id')
        # Deleting all edges before deleting node
        delete_edges = f"DELETE FROM tbl_edge where n1 = '{node_id}' or n2 = '{node_id}'"
        db.execute(delete_edges)
        # Deleting node after all references to it is deleted
        statement = f"DELETE FROM tbl_node WHERE prop_id = '{prop_id}'"
        db.execute(statement)
        return f"Node with prop_id = {prop_id} deleted", 200
