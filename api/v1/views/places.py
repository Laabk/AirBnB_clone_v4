#!/usr/bin/python3
"""this handles the routes Place objects and operations"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place

@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """ acquires all Place obj by city
    :return: json Places"""
    pl_list = []
    c_obj = storage.get("City", str(city_id))
    for objs in c_obj.places:
        pl_list.append(objs.to_json())

    return jsonify(pl_list)
@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """ this will make the place route
    :return: the created Place obj"""
    pl_json = request.get_json(silent=True)
    if pl_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", pl_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in pl_json:
        abort(400, 'Missing user_id')
    if "name" not in pl_json:
        abort(400, 'Missing name')
    pl_json["city_id"] = city_id

    mk_place = Place(**pl_json)
    mk_place.save()
    pl_res = jsonify(mk_place.to_json())
    pl_res.status_code = 201

    return pl_res

@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """ takes a specific Place obj of its id
    :param:the place object id
    :return: place obj or error"""
    fet_obj = storage.get("Place", str(place_id))
    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())

@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """ changes a specific Place object id
    :param:the Place object ID
    :return: the Place object or 404 on failure
    """
    pl_json = request.get_json(silent=True)
    if pl_json is None:
        abort(400, 'Not a JSON')

    fet_obj = storage.get("Place", str(place_id))

    if fet_obj is None:
        abort(404)

    for key, val in pl_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fet_obj, key, val)

    fet_obj.save()

    return jsonify(fet_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """ this deletes Place id
    :param place_id: Place object id
    :return: an empty dict or 404"""

    fet_obj = storage.get("Place", str(place_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
