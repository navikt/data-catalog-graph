from datetime import datetime
from flask import make_response, abort
from sqlalchemy.sql import text
from config import db
from models import Node, NodeSchema


def read_all():
    with db.engine.connect() as con:
        statement = f"SELECT * FROM tbl_node WHERE prop->>'type' = 'GDPR.PURPOSE'"
        terms = con.execute(statement)
        node_schema = NodeSchema(many=True)
        data = node_schema.dump(terms).data
        return data

def read_one(id):
    with db.engine.connect() as con:
        statement = f"SELECT * FROM tbl_node WHERE prop->>'type' = 'GDPR.PURPOSE' AND id = {id}"
        term = con.execute(statement)
    
    if term is not None:
        node_schema = NodeSchema()
        data = node_schema.dump(term).data
        return data
    else:
        abort(404, f"Node with id {id} not found")

