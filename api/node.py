# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


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
    return [NODES[key] for key in sorted(NODES.keys())]


def read_one(id):
    if id in NODES:
        node = NODES.get(id)

    else:
        abort(
            404, "Node with id {id} not found".format(id=id)
        )

    return node

def create(node):
    id = node.get("id", None)
    properties = node.get("properties", {})

    if id not in NODES and id is not None:
        NODES[id] = {
            "id": id,
            "properties": properties
        }
        return NODES[id], 201

    else:
        abort(
            406,
            "Node with id {id} already exists".format(id=id),
        )


def delete(id):
    if id in NODES:
        del NODES[id]
        return make_response(
            "{id} successfully deleted".format(id=id), 200
        )

    else:
        abort(
            404, "Node with id {id} not found".format(id=id)
        )
