from datetime import datetime
from flask import make_response, abort
from config import db
from models import Node, NodeSchema
from database import Database
import re


def get_all():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE prop->>'id' ILIKE 'term.%'"
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes,200

    abort(404, "No terms found")


def search_term_by_name(term_name, term_status):
    db = Database()
    status = term_status
    if status is None:
        status = 'godkjent'

    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' ILIKE 'term.%' AND " \
                f"(prop->>'term' ILIKE '%{term_name}%' OR prop->>'definisjon' ILIKE '%{term_name}%') AND " \
                f"prop->>'status' ILIKE '{status}%' "
    nodes = db.execute(statement)
    pattern = '\[([^|]+)\|([A-Z]{1,10}-\d+)\]'
    if nodes is not None:
        term_list = []
        for term in nodes:
            description = re.sub(pattern, r'\1', term['prop']['definisjon'])
            term_list.append({'id': term['prop']['id'], 'term': term['prop']['term'], 'description': description})

        return term_list, 200

    abort(404, f"No match found with term {term_name}")
