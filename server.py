import os, json

from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from Controllers.dataController import DataFetch


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.json_encoder = json.JSONEncoder

load_dotenv()

fetch_data = DataFetch(place_path=os.getenv("PLACE_PATH"),
                       sort_path=os.getenv("SORT_PATH"),
                       id_path=os.getenv("ID_PATH"))

@app.route("/api/ownapi", methods=["GET"])
def home():
    destin_message = request.args
    if destin_message["target"] == "toilets":
        location = { "lat": destin_message["lat"], "lng": destin_message["lng"] }
        app.logger.info(f"Data request messsage: {location}")
        
        response_data = fetch_data.toilet_around_place(location)
        
        app.logger.info(f"Retrieving data successful: {len(response_data)}")
        return jsonify(response_data), 200
    
    elif destin_message["target"] == "details":
        app.logger.info(destin_message)
        data = fetch_data.parse_tuple_list(parse_list=destin_message)
        response_data = fetch_data.fetch_detail(id_list=data)
        
        app.logger.info(f"Delivering place data successful")
        return jsonify(response_data), 200


if __name__ == "__main__":
    app.run(debug=True)