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
    'n1': 'test_1',
    'n2': 'test_2',
    'guid': 'hashed_id_value',
    'create': 'date_value'
}

EDGES_OLD = {
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
    db = Database()

    statement = "SELECT * FROM tbl_edge"
    print(statement)
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


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
            statement = statement + f"('{n1}', '{n2}'), "

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    # On receiving a prop_id that already exist it will instead update the prop
    statement = statement + " ON CONFLICT (n1, n2) DO UPDATE SET n1 = excluded.n1, n2 = excluded.n2"
    print(statement)
    edge = db.execute(statement)
    return f"Successfully updated {edge} rows", 200

def read_all_edges_of_node(prop_id):
    print("get:",prop_id)
    db = Database()
    
    statement = f"SELECT * FROM tbl_edge WHERE n1={prop_id}"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


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

