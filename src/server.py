from flask import Flask, request, render_template

import get_hotels 
import get_hotel_by_id
from helpers.geo_helper import Point

app = Flask(__name__)

@app.route("/searchresults")
def searchresults():
    return get_hotels.get_hotels(request.args)

@app.route("/hotel")
def hotel():
    return get_hotel_by_id.get_hotel_by_id(request.args)

if __name__=="__main__":
    app.run()
