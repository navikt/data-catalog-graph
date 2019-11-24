from datetime import datetime
from flask import make_response, abort
from config import db
from models import Node, NodeSchema
import json

def read_all():
    with db.engine.begin() as conn:
        result = conn.execute(f"select * from tbl_node limit 5")
        nodes = result.fetchall()
        node_schema = NodeSchema(many=True)
        data = node_schema.dump(nodes).data
        return data

def read_one(id):
    with db.engine.begin() as conn:
        statement = f'select * from tbl_node where "{id}" like "id"'
        print(statement)
        result = conn.execute(statement)
        node = result.fetchone()

        if node is None:
            abort(404, f"Node with id {id} not found")

        node_schema = NodeSchema()
        data = node_schema.dump(node).data
        return data  

def create(node):
    id = node.get("id")
    existing_node = Node.query.filter(Node.id == id).one_or_none()
    
    if existing_node is None:
        schema = NodeSchema()
        new_node = schema.load(node, session=db.session).data

        db.session.add(new_node)
        db.session.commit()

        data = schema.dump(new_node).data
        return data, 201

    else:
        abort(409, f"Node {id} exists already")


def update(id, node):

    update_node = Node.query.filter(Node.id == id).one_or_none()

    if update_node is not None:
        schema = NodeSchema()
        update = schema.load(node, session=db.session).data

        update.id = update_node.id

        db.session.merge(update)
        db.session.commit()

        data = schema.dump(update_node).data
        return data, 200

    else:
        abort(404, f"Node not found for Id: {id}")


def delete(id):
    node = Node.query.filter(Node.node_id == id).one_or_none()

    if node is not None:
        db.session.delete(node)
        db.session.commit()
        return make_response(f"Node {id} deleted", 200)

    else:
        abort(404, f"Node with id {id} not found")
