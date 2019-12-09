# System modules
from datetime import datetime
import json
from database import Database
from flask import make_response, abort

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


def update(edge):
    print("put:", edge)
    statement = "INSERT INTO tbl_edge (n1, n2) VALUES "
    for edge_item in edge:
        n1 = edge_item.get("n1")
        n2 = edge_item.get("n2")
        if n1 is None:
            abort(409, f"The edge must have a n1 key with value of type string")
        if n2 is None:
            abort(409, f"The edge must have a n2 key with value of type string")
        else:
            statement = statement + f"('{json.dumps(n1)}', '{json.dumps(n2)}'), "

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    # On receiving a prop_id that already exist it will instead update the prop
    statement = statement + " ON CONFLICT (n1, n2) DO UPDATE SET n1 = excluded.n1, n2 = excluded.n2"
    print(statement)
    edge = db.execute(statement)
    return f"Successfully updated {edge} rows", 200


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

