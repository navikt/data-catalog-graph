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

def read_one(id):
    db = Database()
    node = db.execute(f"SELECT * FROM tbl_node where id = '{id}'")
    if node is not None:
        return node,201

    abort(404, f"Node with id {id} not found")


def get_by_prop_id(id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node,201

    abort(404, f"Node with prop.id {id} not found")

def create(node):

    print(node)

    prop = node.get("prop")
    if prop is None:
        abort(409, f"The node must have a prop key with value of type dict")

    id = prop.get("id")
    if id is None:
        abort(409, f"The prop dict should contain id property of type string")

    # existing node?
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    node = db.fetchone(statement)
    if node is not None:
        abort(409, f"Node with prop.id {id} already exists: Node id {node.get('id')}")

    #insert new
    db = Database()
    statement =  f"INSERT INTO tbl_node (prop) VALUES ('{json.dumps(prop)}')"
    print(statement)
    db.execute(statement)

    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    node = db.execute(statement)
    if node is not None:
        return node, 201


def update(node):
    print("put:", node)
    node_json = json.loads(json.dumps(node))
    prop = node_json.get('prop')
    id = prop.get("id")
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    update_node = db.fetchone(statement)
    if update_node is None and id is None:
        create(node)

    elif update_node is None:
        abort(409, f"Node with prop.id {id} not found")

    else:
        update_id = update_node.get("id")
        db = Database()
        prop = json.dumps(node.get('prop'))
        statement =  f"UPDATE tbl_node SET prop = ('{prop}') WHERE id = {update_id}"
        db.execute(statement)


def delete(id):
    node = Node.query.filter(Node.node_id == id).one_or_none()

    if node is not None:
        db.session.delete(node)
        db.session.commit()
        return make_response(f"Node {id} deleted", 200)

    else:
        abort(404, f"Node with id {id} not found")
        