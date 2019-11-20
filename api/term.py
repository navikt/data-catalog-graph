from datetime import datetime
from flask import make_response, abort
from config import db
from models import Node, NodeSchema


def read_all():
    terms = Node.query.filter(Node.prop.type == 'term').order_by(Node.id).all()
    node_schema = NodeSchema(many=True)
    data = node_schema.dump(terms).data
    return data

def read_one(id):
    term = Node.query.filter(Node.prop.type == 'term').filter(Node.id == id).one_or_none()
    
    if term is not None:
        node_schema = NodeSchema()
        data = node_schema.dump(term).data
        return data
    else:
        abort(404, f"Node with id {id} not found")

