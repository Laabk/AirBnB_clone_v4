#!/usr/bin/python3
"""
this cares for the Amenity objects
and operations"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """ geting all Amenity objects
    :return: all states"""
    _list = []
    _obj = storage.all("Amenity")
    for objs in _obj.values():
        _list.append(objs.to_json())

    return jsonify(_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """ making and briging theamenity route
    :return: amenity obj"""
    amen_json = request.get_json(silent=True)
    if amen_json is None:
        abort(400, 'Not a JSON')
    if "name" not in amen_json:
        abort(400, 'Missing name')

    _amen = Amenity(**amen_json)
    _amen.save()
    amen_res = jsonify(_amen.to_json())
    amen_res.status_code = 201

    return amen_res
@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """ takes specific Amenity object by an
    :return: obj with id or error"""

    fet_obj = storage.get("Amenity", str(amenity_id))
    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """ changes a specific Amenity object id
    :return: the object amenetei with 200 success
    or 400 or 404 on failure"""
    _json = request.get_json(silent=True)
    if _json is None:
        abort(400, 'Not a JSON')
    fet_obj = storage.get("Amenity", str(amenity_id))
    if fet_obj is None:
        abort(404)
    for key, val in _json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fet_obj, key, val)
    fet_obj.save()
    return jsonify(fet_obj.to_json())
@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """ this deletes Amenity by id
    :param amenity_id: An amenity obj id
    :return: an empty dicti with 200 or 404 if not found
    """

    fet_obj = storage.get("Amenity", str(amenity_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
