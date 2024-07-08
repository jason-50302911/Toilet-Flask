import json

from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from Controllers.dataController import DataFetch


app = Flask(__name__)
cors = CORS(app)
app.json_encoder = json.JSONEncoder

fetch_data = DataFetch(dict_path="data/idDict.json",
                       id_path="data/posid.json")

@app.route("/", methods=['GET', 'POST'])
def get_data():
    destin_message = request.args
    response_data = None
    app.logger.info(destin_message)
    if destin_message["target"] == "toilets":
        bounds = { 
                    "latNorth": destin_message["latNorth"], 
                    "latSouth": destin_message["latSouth"],
                    "lngWest": destin_message["lngWest"],
                    "lngEast": destin_message["lngEast"]
                }
        response_data = fetch_data.inside_bounds_toilet(bounds=bounds)
        app.logger.info(f"Response data length: {len(response_data)}")
    
    elif destin_message["target"] == "details":
        data = fetch_data.parse_tuple_list(parse_list=destin_message)
        response_data = fetch_data.fetch_detail(id_list=data)
        
    elif destin_message["target"] == "finding":
        location = { "lat": destin_message["lat"], "lng": destin_message["lng"] }
        data = fetch_data.toilet_around_place(location=location)
        nearest_data = fetch_data.nearest_toilet(location=location, toilet_list=data)
        app.logger.info(nearest_data["near_loc"])
        response_data = { 
                "toiletData": data,
                "nearest_uuid": nearest_data["nearest_uuid"],
                "distance": nearest_data["distance"],
                "near_loc": nearest_data["near_loc"]
            }
        
    if response_data is None:
        app.logger.info(f"Error: Fail to fetch data")
        return jsonify("Bad request: wrong request message"), 404
    else:
        app.logger.info(f"Delivering place data successful")
        return jsonify(response_data), 200
    
@app.route("/paid")
def paid_page():
    return render_template("./paidPage.html")
    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')