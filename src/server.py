from flask import Flask, request

import get_hotels 
from helpers.geo_helper import Point

app = Flask(__name__)

@app.route("/")
def hello():
    print(request.args.to_dict())
    return get_hotels.get_hotels(request.args)

if __name__=="__main__":
    app.run()
