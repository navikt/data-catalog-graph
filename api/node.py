from datetime import datetime
from flask import make_response, abort
from config import db
from models import Node, NodeSchema


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


NODES = {
    "1": {
        "id": "1",
        "properties": {"type": "term", "versions": [{
            "version": 1, 
            "validfrom": "2019-1-1", 
            "validto": "2099-12-31",
            "current": True, 
            "properties": {"name": "term name", "description": "term description"}
        }]
    }},
    "2": {
        "id": "2",
        "properties": {"type": "term", "versions": [{
            "version": 1, 
            "validfrom": "2019-1-1", 
            "validto": "2099-12-31",
            "current": True, 
            "properties": {"name": "term name", "description": "term description"}
        }]
    }},
    "3": {
        "id": "3",
        "properties": {"type": "term", "versions": [{
            "version": 1, 
            "validfrom": "2019-1-1", 
            "validto": "2099-12-31",
            "current": True, 
            "properties": {"name": "term name", "description": "term description"}
        }]
    }}
}

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
        abort(
            404, "Node with id {id} not found".format(id=id)
        )


def create(node):
    id = node.get("id")
    existing_node = Node.query.filter(Node.id == id).one_or_none()
    
    if existing_node is None:
        schema = NodeSchema()
        new_node = schema.load(node, session=db.session).data

        # Add the node to the database
        db.session.add(new_node)
        db.session.commit()

        # Serialize and return the newly created node in the response
        data = schema.dump(new_node).data

        return data, 201

    else:
        abort(409, f"Node {id} exists already")


def delete(id):
    node = Node.query.filter(Node.node_id == id).one_or_none()

    if node is not None:
        db.session.delete(node)
        db.session.commit()
        return make_response(f"Node {id} deleted", 200)

    else:
        abort(
            404, "Node with id {id} not found".format(id=id)
        )
