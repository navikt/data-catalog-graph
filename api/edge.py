# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


EDGES = {
    "1": {
        "id": "1",
        "start": "2",
        "end": "3",
        "properties": {"type": "defined by term", "versions": [{
            "version": 1, 
            "validfrom": "2019-1-1", 
            "validto": "2099-12-31",
            "current": True
        }]
    }},
    "2": {
        "id": "2",
        "start": "3",
        "end": "2",
         "properties": {"type": "term defines", "versions": [{
            "version": 1, 
            "validfrom": "2019-1-1", 
            "validto": "2099-12-31",
            "current": True
        }]
    }}
}

def read_all():
    return [EDGES[key] for key in sorted(EDGES.keys())]


def read_one(id):
    if id in EDGES:
        node = EDGES.get(id)

    else:
        abort(
            404, "Edge with id {id} not found".format(id=id)
        )

    return node

def delete(id):
    if id in EDGES:
        del EDGES[id]
        return make_response(
            "{id} successfully deleted".format(id=id), 200
        )

    else:
        abort(
            404, "Edge with id {id} not found".format(id=id)
        )

