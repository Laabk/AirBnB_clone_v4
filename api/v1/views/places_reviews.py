#!/usr/bin/python3
""" this handles the review objects and operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """ acquires all review objects by the place
    :return: jsons reviews"""
    rw_list = []
    pl_obj = storage.get("Place", str(place_id))
    if pl_obj is None:
        abort(404)

    for objes in pl_obj.reviews:
        rw_list.append(objes.to_json())
    return jsonify(rw_list)

@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """this makes the review route involved
    :return: the created Review obj"""
    rw_json = request.get_json(silent=True)
    if rw_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", rw_json["user_id"]):
        abort(404)
    if "user_id" not in rw_json:
        abort(400, 'Missing user_id')
    if "text" not in rw_json:
        abort(400, 'Missing text')
    rw_json["place_id"] = place_id
    mk_revw = Review(**rw_json)
    mk_revw.save()
    rw_res = jsonify(mk_revw.to_json())
    rw_res.status_code = 201

    return rw_res


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """ takes a specific Review object id 
    :param: the place object id
    :return: the review obj or an error"""

    fet_obj = storage.get("Review", str(review_id))
    if fet_obj is None:
        abort(404)
    return jsonify(fet_obj.to_json())

@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """ changes some specific Review object id
    :param: the review object ID
    :return: the review object or 404 on failure"""
    pl_json = request.get_json(silent=True)

    if pl_json is None:
        abort(400, 'Not a JSON')

    fet_obj = storage.get("Review", str(review_id))

    if fet_obj is None:
        abort(404)

    for keys, val in pl_json.items():
        if keys not in ["id", "created_at", "updated_at", "user_id",
                        "place_id"]:
            setattr(fet_obj, keys, val)

    fet_obj.save()

    return jsonify(fet_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """ this deletes Review by id
    :param :thee review object id
    :return: an empty dictin..or 404 if not found"""

    fet_obj = storage.get("Review", str(review_id))

    if fet_obj is None:
        abort(404)

    storage.delete(fet_obj)
    storage.save()

    return jsonify({})
