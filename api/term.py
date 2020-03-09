from flask import abort
from database import Database
import re


def get_all():
    db = Database()
    statement = "SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p " \
                "WHERE p.valid = TRUE AND p.prop->>'type' ILIKE 'term' " \
                "AND prop->>'status' ILIKE 'godkjent%' AND n.prop_id = p.prop->>'id'"
    nodes = db.execute(statement)

    if nodes is not None:
        return nodes,200

    abort(404, "No terms found")


def get_valid_node_by_prop_id(id):
    db = Database()
    statement = f"SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p " \
                f"WHERE p.valid = TRUE AND p.prop->>'type' ILIKE 'term' AND n.prop_id = p.prop->>'id' " \
                f"AND p.prop->>'id' = '{id}'"

    nodes = db.execute(statement)
    pattern_with_site_link = '\[([^|]+)\|((www.jira|http:\/\/jira|https:\/\/jira|http:\/\/www.jira|https:\/\/www' \
                             '.jira)+[^\s]+[\w])\]'
    pattern = '\[([^|]+)\|([A-Z]{1,10}-\d+)\]'
    if nodes is not None:
        for term in nodes:
            filtered_description = re.sub(pattern, r'\1', term['prop']['definisjon'])
            description_without_site_links = re.sub(pattern_with_site_link, r'\1', filtered_description)
            term.update({'node_id': term['id']})
            term.update({'id': term['prop']['id']})
            term.update({'term': term['prop']['term']})
            term.update({'description': description_without_site_links})
            term.update({'status': term['prop']['status']})

        return nodes, 200

    abort(404, f"Node with prop.id {id} not found")


def search_term_by_name(term_name, term_status='godkjent'):
    db = Database()

    statement = f"""SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p 
                    WHERE p.valid = TRUE AND p.prop->>'type' ILIKE 'term' AND n.prop_id = p.prop->>'id' AND
                  (p.prop->>'term' ILIKE '%{term_name}%' OR p.prop->>'definisjon' ILIKE '%{term_name}%') AND 
                  p.prop->>'status' ILIKE '%{term_status}%' """
    nodes = db.execute(statement)
    pattern_with_site_link = '\[([^|]+)\|((www.jira|http:\/\/jira|https:\/\/jira|http:\/\/www.jira|https:\/\/www' \
                             '.jira)+[^\s]+[\w])\]'
    pattern = '\[([^|]+)\|([A-Z]{1,10}-\d+)\]'
    if nodes is not None:
        for term in nodes:
            filtered_description = re.sub(pattern, r'\1', term['prop']['definisjon'])
            description_without_site_links = re.sub(pattern_with_site_link, r'\1', filtered_description)
            term.update({'node_id': term['id']})
            term.update({'id': term['prop']['id']})
            term.update({'term': term['prop']['term']})
            term.update({'description': description_without_site_links})
            term.update({'status': term['prop']['status']})

        return nodes, 200

    abort(404, f"No match found with term {term_name}")
