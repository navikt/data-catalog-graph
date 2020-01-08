from flask import abort
from database import Database


def get_all_valid_kafka_topic():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'kafka_topic'"
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No kafka topics found")


def get_all_valid_kafka_topic_field():
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'kafka_topic_field'"
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, "No kafka topic fields found")


def get_valid_kafka_topic_by_prop_id(prop_id):
    db = Database()
    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'kafka_topic' 
                    AND prop->>'id' = '{prop_id}'"""
    print(statement)
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Kafka topic with prop id {prop_id} not found")


def get_valid_kafka_topic_field_by_prop_id(prop_id):
    db = Database()
    statement = f"""SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE 'kafka_topic_field' 
                    AND prop->>'id' = '{prop_id}'"""
    print(statement)
    nodes = db.execute(statement)

    if len(nodes) >= 1:
        return nodes, 200

    abort(404, f"Kafka topic field with prop id {prop_id} not found")
