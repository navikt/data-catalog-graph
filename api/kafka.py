import json

from flask import abort
from database import Database


def get_all_valid_kafka_topic_fields(prop_id):
    db = Database()
    statement = f"""SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid,
                    e.n1 source_node, e.n2 target_node, e.prop edge_prop, e.created edge_created 
                    FROM tbl_node n, tbl_edge e, tbl_node_prop p 
                    WHERE n.prop_id = p.prop->>'id' AND n.id = e.n2 AND p.valid = TRUE 
                    AND p.prop->>'type' = 'kafka_topic_field'
                    AND n.id IN (SELECT n2 FROM tbl_edge WHERE  n1 =
                    (SELECT id FROM tbl_node WHERE prop_id = '{prop_id}'))
                    ORDER BY n.prop->>'field_name' ;"""
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No kafka topic fields found")


def get_all_valid_kafka_topic():
    db = Database()
    statement = """SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p 
                    WHERE n.prop_id = p.prop->>'id' AND p.valid = TRUE AND p.prop->>'type' ILIKE 'kafka_topic'"""
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No kafka topics found")


def get_all_valid_kafka_topic_field():
    db = Database()
    statement = """SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p 
                    WHERE n.prop_id = p.prop->>'id' AND p.valid = TRUE AND p.prop->>'type' ILIKE 'kafka_topic_field'"""
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No kafka topic fields found")


def get_valid_kafka_topic_by_prop_id(prop_id):
    db = Database()
    statement = f"""SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p 
                    WHERE n.prop_id = p.prop->>'id' AND p.valid = TRUE AND p.prop->>'type' ILIKE 'kafka_topic' 
                    AND n.prop_id = '{prop_id}'"""

    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Kafka topic with prop id {prop_id} not found")


def get_valid_kafka_topic_field_by_prop_id(prop_id):
    db = Database()
    statement = f"""SELECT n.id, p.prop, p.valid_from, p.valid_to, p.valid FROM tbl_node n, tbl_node_prop p 
                    WHERE n.prop_id = p.prop->>'id' AND p.valid = TRUE AND p.prop->>'type' ILIKE 'kafka_topic_field' 
                    AND n.prop_id = '{prop_id}'"""

    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Kafka topic field with prop id {prop_id} not found")
