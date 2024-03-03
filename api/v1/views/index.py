#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """ the status route of the api involved
    :return: json responses"""
    api_statu = {"status": "OK"}

    amen_res = jsonify(api_statu)
    amen_res.status_code = 200

    return amen_res


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """the different stats of the objs route
    :return: the json objs"""
    api_statu = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    api_res = jsonify(api_statu)
    api_res.status_code = 200
    return api_res
