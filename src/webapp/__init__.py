from flask import Flask, request, render_template

import webapp.handlers.get_hotels as get_hotels
import webapp.handlers.get_hotel_by_id as get_hotel_by_id
from webapp.helpers.geo_helper import Point

def create_app():

    app = Flask(__name__)

    @app.route("/searchresults")
    def searchresults():
        return get_hotels.get_hotels(request.args)

    @app.route("/hotel")
    def hotel():
        return get_hotel_by_id.get_hotel_by_id(request.args)

    return app
