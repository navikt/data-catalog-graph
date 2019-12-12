from datetime import datetime
from flask import make_response, abort
from config import db
from models import Node, NodeSchema
from database import Database
import re


def get_all():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE prop->>'id' LIKE 'term.%'"
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes,200

    abort(404, "No terms found")


def search_term_by_name(term_name):
    db = Database()
    statment = f"SELECT * FROM tbl_node WHERE prop->>'id' LIKE 'term.%' AND prop->>'term' LIKE '{term_name}%'"
    nodes = db.execute(statment)
    pattern = '\[([^|]+)\|([A-Z]{1,10}-\d+)\]'
    if nodes is not None:
        term_list = []
        for term in nodes:
            name = term['prop']['term']
            description = re.sub(pattern, r'\1',term['prop']['definisjon'])
            term_list.append({'term': name, 'description': description})

        return term_list, 200

    abort(404, f"No match found with term {term_name}")