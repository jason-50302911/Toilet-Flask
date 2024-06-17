import json

from flask_cors import CORS
from flask import Flask, request, jsonify
from Controllers.dataController import DataFetch


app = Flask(__name__)
cors = CORS(app)
app.json_encoder = json.JSONEncoder

fetch_data = DataFetch(dict_path="data/idDict.json",
                       id_path="data/posid.json")

@app.route("/", methods=['GET'])
def get_data():
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
    else:
        return jsonify("welcome to the Jason google map"), 200
    

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')