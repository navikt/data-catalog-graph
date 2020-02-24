# System modules
import json
from database import Database
from flask import abort


def get_all():
    db = Database()

    statement = "SELECT * FROM tbl_edge"
    print(statement)
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def update(edges):
    print("put:", edges)
    statement = "WITH valid_nodes as (SELECT id, prop->>'id' as prop_id from tbl_node WHERE valid = TRUE ) " \
                "INSERT INTO tbl_edge (n1, n2, prop) VALUES"
    for edge in edges:
        n1 = edge.get("n1")
        n2 = edge.get("n2")
        prop = json.dumps(edge.get("prop"))
        if n1 is None:
            abort(409, f"The edge must have a source node n1 of type string")
        if n2 is None:
            abort(409, f"The edge must have a target node n2 of type string")
        if prop is None:
            abort(409, f"The edge must have a prop with value of type dict")
        else:
            json_prop = prop.replace("\'", "''")
            statement = statement + f""" ((SELECT id FROM valid_nodes WHERE prop_id = '{n1}'), 
                                        (SELECT id FROM valid_nodes WHERE prop_id = '{n2}'), 
                                        '{json_prop}'::jsonb),"""

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-1]
    # On receiving a prop_id that already exist it will instead update the prop
    statement = statement + " ON CONFLICT (n1, n2) DO UPDATE SET prop = tbl_edge.prop || excluded.prop RETURNING n1"
    edge = db.execute(statement)
    return f"Successfully updated {len(edge)} rows", 200


def get_all_edges_of_node(node_id):
    print("get:", node_id)
    db = Database()
    
    statement = f"SELECT * FROM tbl_edge WHERE n1 = {node_id} OR n2 = {node_id}"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def get_all_edges_of_source_node(node_id):
    print("get:", node_id)
    db = Database()

    statement = f"""SELECT n.*, e.n1 source_node, e.n2 target_node, e.prop edge_prop, e.created edge_created 
                    FROM tbl_node n, tbl_edge e 
                    WHERE n.id = e.n2 AND n.valid = TRUE AND n.id IN (SELECT n2 FROM tbl_edge WHERE n1 = {node_id});"""
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def get_all_edges_of_target_node(node_id):
    print("get:", node_id)
    db = Database()

    statement = f"SELECT * FROM tbl_edge WHERE n2={node_id}"
    edges = db.execute(statement)

    if edges is not None:
        return edges, 200

    abort(404, "Error fetching edges")


def delete(n1, n2):
    db = Database()

    statement = f"DELETE FROM tbl_edge WHERE n1={n1} AND n2 = {n2}'"
    delete_edge = db.execute(statement)

    if delete_edge is not None:
        return f"Successfully deleted {delete_edge} edge", 200

    abort(404, "Error deleting edge")
