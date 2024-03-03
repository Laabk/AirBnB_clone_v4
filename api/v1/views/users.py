#!/usr/bin/python3
"""this handles the User objects and operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """ takes all the User objects
    :return: users in json"""
    ur_list = []
    ur_obj = storage.all("User")
    for objes in ur_obj.values():
        ur_list.append(objes.to_json())
    return jsonify(ur_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """ this makes the user route
    :return: the created user obj"""
    ur_json = request.get_json(silent=True)
    if ur_json is None:
        abort(400, 'Not a JSON')
    if "email" not in ur_json:
        abort(400, 'Missing email')
    if "password" not in ur_json:
        abort(400, 'Missing password')
    nw_user = User(**ur_json)
    nw_user.save()
    ur_res = jsonify(nw_user.to_json())
    ur_res.status_code = 201
    return ur_res

@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """ takes some specific User object id
    :param: the user object id
    :return: the user obj or error"""

    fet_obj = storage.get("User", str(user_id))
    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())

@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def put_user_func(user_id):
    """this changes specific User object by ID
    :param: the user object ID
    :return: the user object or 400 or 404 on failure
    """
    ur_json = request.get_json(silent=True)

    if ur_json is None:
        abort(400, 'Not a JSON')

    fet_obj = storage.get("User", str(user_id))

    if fet_obj is None:
        abort(404)

    for keys, val in ur_json.items():
        if keys not in ["id", "created_at", "updated_at", "email"]:
            setattr(fet_obj, keys, val)
    fet_obj.save()

    return jsonify(fet_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """ this deletes the User by id
    :param: the user object id
    :return: an empty dict or 404 if not found
    """

    fet_obj = storage.get("User", str(user_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
