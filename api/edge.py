# System modules
import json
from database import Database
from flask import make_response, abort
import logging


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
    db = Database()
    statement = "INSERT INTO tbl_edge (n1, n2, prop) VALUES "
    for edge_item in edge:
        n1 = edge_item.get("n1")
        n2 = edge_item.get("n2")
        prop = edge_item.get("prop")
        if n1 is None:
            abort(409, f"The edge must have a n1 key with value of type string")
        if n2 is None:
            abort(409, f"The edge must have a n2 key with value of type string")
        if prop is None:
            abort(409, f"The edge must have a prop key with value of type string")
        else:
            n1_id = json.dumps(db.execute(f"SELECT id FROM tbl_node WHERE prop_id = '{n1}'"))
            n2_id = json.dumps(db.execute(f"SELECT id FROM tbl_node WHERE prop_id = '{n2}'"))
            json_prop = json.dumps(prop).replace("\'", "''")
            statement = statement + f"({n1_id[0]['id']}, {n2_id[0]['id']}, '{json_prop}'::jsonb), "

    # insert new

    # Deleting the space and ',' at the end of the statement
    statement = statement[:-2]
    # On receiving a prop_id that already exist it will instead update the prop
    statement = statement + " ON CONFLICT (n1, n2) DO UPDATE SET prop = tbl_edge.prop || excluded.prop RETURNING n1"
    print(statement)
    edge = db.execute(statement)
    return f"Successfully updated {len(edge)} rows", 200


def read_all_edges_of_node(prop_id):
    print("get:",prop_id)
    db = Database()
    
    statement = f"SELECT * FROM tbl_edge WHERE n1='{prop_id}'"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def delete(guid):
    db = Database()

    statement = f"DELETE FROM tbl_edge WHERE guid='{guid}'"
    delete_edge = db.execute(statement)

    if delete_edge is not None:
        return f"Successfully deleted {delete_edge} edge", 200

    abort(404, "Error deleting edge")
