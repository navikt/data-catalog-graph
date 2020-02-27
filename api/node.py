import logging
import json
from flask import abort
from database import Database


def get_all():
    db = Database()
    nodes = db.execute(f"SELECT * FROM tbl_node")
    if nodes is not None:
        return nodes

    abort(404, f"Error fetching nodes")


def get_all_valid():
    db = Database()
    nodes = db.execute(f"SELECT * FROM tbl_node where valid = TRUE")
    if nodes is not None:
        return nodes

    abort(404, f"Error fetching nodes")


def get_by_id(id):
    db = Database()
    node = db.execute(f"SELECT * FROM tbl_node WHERE id = '{id}'")
    if node is not None:
        return node, 200

    abort(404, f"Node with guid {id} not found")


def get_by_prop_id(id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{id}'"
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"Node with prop.id {id} not found")


def get_valid_node_by_prop_id(id):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'id' = '{id}'"
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"Node with prop.id {id} not found")


def get_all_nodes_by_type(type):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE prop->>'type' ILIKE '{type}' "
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"No node found with prop_id matching {type}")


def get_all_valid_nodes_by_type(type):
    db = Database()
    statement = f"SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'type' ILIKE '{type}' "
    print(statement)
    node = db.execute(statement)
    if node is not None:
        return node, 200

    abort(404, f"No node found with prop_id matching {type}")


def get_nodes_by_list_of_ids(id_list):
    logging.warning(id_list)
    db = Database()
    statement = "SELECT * FROM tbl_node WHERE id IN ("
    for list_item in id_list:
        if list_item is None:
            abort(400, f"Request body is missing ID key of type integer")
        statement = statement + f' {list_item},'

    #DELETE the last "," in statement
    statement = statement[:-1]
    statement = statement + ");"
    print(statement)
    nodes = db.execute(statement)
    return nodes, 200


def create(node):
    print(node)
    statement = "INSERT INTO tbl_node (prop, valid) VALUES"
    for node_item in node:
        prop = node_item.get("prop")
        if prop is None:
            abort(409, f"The node must have a prop key with value of type dict")
        prop_id = prop.get("id")
        if prop_id is None:
            abort(409, f"The prop dict should contain id property of type string")
        prop_type = prop.get("type")
        if prop_type is None:
            abort(409, f"The prop dict should contain type property of type string")
        else:
            json_prop = json.dumps(prop).replace("\'", "''")
            statement = statement + f" ('{json_prop}', TRUE),"

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of the statement
    statement = statement[:-1]
    print(statement)
    node = db.execute(statement)
    return f" Successfully created {node} rows", 200


def upsert_node(node):
    print("put:", node)
    statement = "WITH previous_valid AS (SELECT * FROM tbl_node WHERE valid = TRUE AND prop->>'id' IN ("
    update_statement = "update_previous_valid AS (UPDATE tbl_node SET valid_to = now(), valid = FALSE " \
                       "WHERE valid_to IS Null AND id IN (SELECT id from previous_valid))"
    create_statement = "INSERT INTO tbl_node (prop, valid) VALUES"
    for node_item in node:
        prop = node_item.get("prop")
        if prop is None:
            abort(409, f"The node must have a prop key with value of type dict")
        prop_id = prop.get("id")
        if prop_id is None:
            abort(409, f"The prop dict should contain id property of type string")
        prop_type = prop.get("type")
        if prop_type is None:
            abort(409, f"The prop dict should contain type property of type string")
        else:
            json_prop = json.dumps(prop).replace("\'", "''")
            statement = statement + f" '{prop_id}',"
            create_statement = create_statement + f"""(COALESCE((SELECT prop FROM previous_valid WHERE prop->>'id' = 
                                                '{prop_id}')::jsonb, """ + "'{}'::jsonb) ||" \
                                                + f" '{json_prop}'::jsonb, TRUE),"

    # insert new
    db = Database()
    # Deleting the space and ',' at the end of each statement
    statement = statement[:-1]
    statement = statement + ")),"
    create_statement = create_statement[:-1]
    statement = statement + update_statement + create_statement
    print(statement)
    # Creating new nodes with valid states
    node = db.execute(statement)
    return f"Successfully updated {node} rows", 200


def delete(prop_id):
    print("delete:", prop_id)

    # Checking if node with prop_id exist
    db = Database()
    check_statement = f"SELECT * FROM tbl_node WHERE prop->>'id' = '{prop_id}'"
    node = db.execute(check_statement)
    if node is None:
        abort(404, f"Could not find node with prop->>'id' = '{prop_id}'")
    else:
        node_id = node.get('id')
        # Deleting all edges before deleting node
        delete_edges = f"DELETE FROM tbl_edge where n1 = {node_id} or n2 = {node_id}"
        db.execute(delete_edges)
        # Deleting node after all references to it is deleted
        statement = f"DELETE FROM tbl_node WHERE prop->>'id' = '{prop_id}'"
        db.execute(statement)
        return f"Node with prop id = {prop_id} deleted", 200


def add_node_comment(node):

    node_id = node.get("nodeId")
    if node_id is None:
        abort(409,  "The node should contain a node Id property of type integer")
    comment = node.get("commentBody")
    if comment is None:
        abort(409,  "The node should contain comment property of type dict")
    comment_id = comment.get("id")
    if comment_id is None:
        abort(409,  "The comment dict should contain id property of type string")
    comment_author = comment.get("author")
    if comment_author is None:
        abort(409, "The comment dict should contain author property of type string")

    db = Database()
    json_comment = json.dumps(comment).replace("\'", "''")
    statement = "UPDATE tbl_node SET prop = jsonb_insert(prop, '{comments, 0}',"
    statement = statement + f"""'{json_comment}'::jsonb) WHERE id = {node_id}"""

    #check if node has comments.
    check_statement = f"SELECT prop->>'comments' AS comments FROM tbl_node WHERE id = {node_id}"
    check_result = db.execute(check_statement)
    logging.warning(check_result)
    #creates comment key if it does not exist.
    if check_result is None:
        logging.warning("if clause triggered")
        comment_list = '{"comments": []}'
        create_comment_list = f"UPDATE tbl_node SET prop = prop::jsonb || '{comment_list}'::jsonb WHERE id = {node_id};"
        statement = create_comment_list + statement

    logging.warning(statement)
    response = db.execute(statement)
    return f" Successfully added {response} comment ", 200


def delete_node_comment(commentId, nodeId):
    if commentId is None:
        abort(409,  "The query should contain comment id property of type string")
    if nodeId is None:
        abort(409,  "The query should contain a node id property of type integer")
    print("delete comment:", commentId)

    db = Database()
    statement = f"""WITH new_comment_list AS (SELECT list FROM tbl_node n, jsonb_array_elements(prop->'comments') list
                    WHERE n.id = {nodeId} AND list->>'id' NOT IN ('{commentId}')), 
                    update_node AS (UPDATE tbl_node SET prop = prop::jsonb - 'comments' WHERE id = {nodeId})
                    UPDATE tbl_node SET prop = prop::jsonb || (SELECT jsonb_build_object('comments', 
                    json_agg(list)::jsonb) FROM new_comment_list) WHERE id = {nodeId}"""
    print(statement)
    db.execute(statement)
    return f" comment id = {commentId} deleted", 200
