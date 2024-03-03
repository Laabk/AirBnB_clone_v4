#!/usr/bin/python3
""" this handles State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """ this acquires City obj from a specific state
    :return: json cities in a state or 404 on error"""
    c_list = []
    st_obj = storage.get("State", state_id)
    if st_obj is None:
        abort(404)
    for objs in st_obj.cities:
        c_list.append(objs.to_json())
    return jsonify(c_list)

@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """ making the city route
    param: state_id - state id
    :return: the created city obj
    """
    c_json = request.get_json(silent=True)
    if c_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)
    if "name" not in c_json:
        abort(400, 'Missing name')
    c_json["state_id"] = state_id

    mk_city = City(**c_json)
    mk_city.save()
    c_res = jsonify(mk_city.to_json())
    c_res.status_code = 201

    return c_res

@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """ tkaes specific City object by ID
    :param city_id: the city object id
    :return: the city obj with an id or error"""

    fet_obj = storage.get("City", str(city_id))

    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())

@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """ changes the specific City object by id
    :param city_id: the city object id
    :return: the city object """
    c_json = request.get_json(silent=True)
    if c_json is None:
        abort(400, 'Not a JSON')
    fet_obj = storage.get("City", str(city_id))
    if fet_obj is None:
        abort(404)
    for key, val in c_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fet_obj, key, val)
    fet_obj.save()
    return jsonify(fet_obj.to_json())

@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """ this deletes City by the id
    :param: the city object id
    :return: an empty dict with 200 or 404 if not found
    """
    fet_obj = storage.get("City", str(city_id))
    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
