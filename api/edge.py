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


def get_all():
    db = Database()

    statement = "SELECT * FROM tbl_edge"
    print(statement)
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def update(edges):
    statement = "INSERT INTO tbl_edge (n1, n2, prop) VALUES "

    for edge in edges:
        n1 = edge.get("n1")
        n2 = edge.get("n2")
        prop = json.dumps(edge.get("prop"))
        if n1 is None:
            abort(409, f"The edge must have a source node n1 of type string")
        if n2 is None:
            abort(409, f"The edge must have a target node n2 of type string")
        if prop is None:
            abort(409, f"The edge must have a prop of type string")
        else:
            statement = statement + f"({n1}, {n2}, '{prop}'), "

    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    # TODO: add not overwrite prop
    # On receiving a pair of nodes that already exist it will add the prop to the prop array
    statement = statement + " ON CONFLICT (n1, n2) DO UPDATE SET n1 = excluded.n1, n2 = excluded.n2, prop=excluded.prop"
    print(statement)
    edge = db.execute(statement)
    return f"Successfully updated {len(edge)} rows", 200

def get_all_edges_of_node(node_id):
    print("get:",node_id)
    db = Database()
    
    statement = f"SELECT * FROM tbl_edge WHERE n1='{node_id}' OR n2='{node_id}'"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")

def get_all_edges_of_source_node(node_id):
    print("get:",node_id)
    db = Database()
    
    statement = f"SELECT * FROM tbl_edge WHERE n1='{node_id}'"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")

def get_all_edges_of_target_node(node_id):
    print("get:",node_id)
    db = Database()
    
    statement = f"SELECT * FROM tbl_edge WHERE n2='{node_id}'"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def delete(guid):
    db = Database()

    statement = f"DELETE FROM tbl_edge WHERE guid='{guid}'"
    delete_edge = db.execute(statement)

    if delete_edge is not None:
        return delete_edge, 200

    abort(404, "Error deleting edge")
