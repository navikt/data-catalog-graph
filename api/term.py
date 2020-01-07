from flask import abort
from database import Database
import re


def get_all():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'term'"
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes,200

    abort(404, "No terms found")


def get_valid_node_by_prop_id(id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'term' AND prop->>'id' = '{id}'"
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"Node with prop.id {id} not found")


def search_term_by_name(term_name, term_status='godkjent'):
    db = Database()

    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'term' AND 
                  (prop->>'term' ILIKE '%{term_name}%' OR prop->>'definisjon' ILIKE '%{term_name}%') AND 
                  prop->>'status' ILIKE '{term_status}%' """
    nodes = db.execute(statement)
    pattern = '\[([^|]+)\|([A-Z]{1,10}-\d+)\]'
    if nodes is not None:
        term_list = []
        for term in nodes:
            description = re.sub(pattern, r'\1', term['prop']['definisjon'])
            term_list.append({
                'id': term['prop']['id'],
                'term': term['prop']['term'],
                'description': description,
                'status': term['prop']['status'],
                'prop': term['prop']
            })

        return term_list, 200

    abort(404, f"No match found with term {term_name}")
