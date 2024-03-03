#!/usr/bin/python3
""" this handles the State objects and operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """ takes all the State objects
    :return: all states in json"""
    st_list = []
    sta_obj = storage.all("State")
    for objes in sta_obj.values():
        st_list.append(objes.to_json())

    return jsonify(st_list)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """ this makes the state route
    :return: the created state obj"""
    sta_json = request.get_json(silent=True)
    if sta_json is None:
        abort(400, 'Not a JSON')
    if "name" not in sta_json:
        abort(400, 'Missing name')
    mk_state = State(**sta_json)
    mk_state.save()
    sta_res = jsonify(mk_state.to_json())
    sta_res.status_code = 201
    return sta_res


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """ takes a specific State object by id
    :param: the state object id
    :return: a state obj or error"""
    fet_obj = storage.get("State", str(state_id))

    if fet_obj is None:
        abort(404)

    return jsonify(fet_obj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """ this takes specific State object in id
    :param: state object id
    :return: an state object or 404 on failure"""
    sta_json = request.get_json(silent=True)
    if sta_json is None:
        abort(400, 'Not a JSON')
    fet_obj = storage.get("State", str(state_id))
    if fet_obj is None:
        abort(404)
    for keys, val in sta_json.items():
        if keys not in ["id", "created_at", "updated_at"]:
            setattr(fet_obj, keys, val)
    fet_obj.save()
    return jsonify(fet_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """ this deletes State id which is involved
    :param : the state object id
    :return: an empty dict or 404 if not found
    """

    fet_obj = storage.get("State", str(state_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
