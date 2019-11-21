from datetime import datetime
import json
from flask import make_response, abort
from config import db
from models import Node, NodeSchema


def read_all():
    nodes = Node.query.order_by(Node.id).all()
    node_schema = NodeSchema(many=True)
    data = node_schema.dump(nodes).data
    return data

def read_one(id):
    node = (
        Node.query.filter(Node.id == id).one_or_none()
    )

    if node is not None:
        node_schema = NodeSchema()
        data = node_schema.dump(node).data
        return data
    else:
        abort(404, f"Node with id {id} not found")


def get_by_prop_id(id):
    node = (
        Node.query.filter(Node.id == id).one_or_none()
    )

    if node is not None:
        node_schema = NodeSchema()
        data = node_schema.dump(node).data
        return data
    else:
        abort(404, f"Node with id {id} not found")

def create(node):

    prop = node.get("prop")
    if prop is None:
        abort(409, f"The node must have a prop key with value of type dict")

    id = prop.get("id")
    if id is None:
        abort(409, f"The prop dict should contain id property of type string")

    # update existing
    with db.engine.connect() as con:
        statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
        terms = con.execute(statement)
        node_schema = NodeSchema(many=True)
        data = node_schema.dump(terms).data
        if len(data):
            for item in data:
                print(item)

            return data[0], 201

    #insert new
    with db.engine.connect() as con:
        prop =  json.dumps(prop)
        statement =  f"INSERT INTO tbl_node (prop) VALUES ('{prop}')"
        con.execute(statement)
        statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
        terms = con.execute(statement)
        node_schema = NodeSchema(many=True)
        data = node_schema.dump(terms).data
        if len(data):
            return data[0], 201

    
def update(id, node):

    update_node = Node.query.filter(Node.prop.id == id).one_or_none()

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
        