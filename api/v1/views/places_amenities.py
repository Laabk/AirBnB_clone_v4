#!/usr/bin/python3
"""this handles the place and amenities linking"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """takesamenities of a place
    :param: the amenity id
    :return: the amenities"""
    fet_obj = storage.get("Place", str(place_id))
    the_amenities = []

    if fet_obj is None:
        abort(404)

    for objs in fet_obj.amenities:
        the_amenities.append(objs.to_json())
    return jsonify(the_amenities)

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """ this stops and unlinks an amenity in a place
    :param: the place id
    :param: the amenity id
    :return: An empty dict or error
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id))
        abort(404)

    fet_obj = storage.get("Place", place_id)
    get = 0

    for objes in fet_obj.amenities:
        if str(objes.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fet_obj.amenities.remove(objes)
            else:
                fet_obj.amenity_ids.remove(objes.id)
            fet_obj.save()
            get = 1
            break

    if get == 0:
        abort(404)
    else:
        st_res = jsonify({})
        st_res.status_code = 201
        return st_res

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """ connecting the amenity with a place
    :param: the place id
    :param: the amenity id
    :return: the Amenity obj or an error
    """
    fet_obj = storage.get("Place", str(place_id))
    ame_obj = storage.get("Amenity", str(amenity_id))
    get_ame = None

    if not fet_obj or not ame_obj:
        abort(404)

    for objs in fet_obj.amenities:
        if str(objs.id) == amenity_id:
            get_ame = objs
            break
    if get_ame is not None:
        return jsonify(get_ame.to_json())
    if getenv("HBNB_TYPE_STORAGE") == "db":
        fet_obj.amenities.append(ame_obj)
    else:
        fet_obj.amenities = ame_obj

    fet_obj.save()

    ame_res = jsonify(ame_obj.to_json())
    ame_res.status_code = 201

    return ame_res
