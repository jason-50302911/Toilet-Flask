import os
import numpy as np
import math

from Controllers.readDataController import read_json
from DataProcess.positionProcess import id_encoder
from typing import Union
from geopy.distance import geodesic

class DataFetch:
    def __init__(self, dict_path, id_path):
        self.dict_file = read_json(dict_path)
        self.id_file = read_json(id_path)
    
    def find_id_list(self, id_list: list[str]) -> list:
        data = []
        for id in id_list: 
            detail_list = self.dict_file[id[0]][id[1:3]]
            for detail in detail_list:
                if detail["number"] == id:
                    data.append(detail)
        return data
    
    def parse_tuple_list(self, parse_list: list[tuple]) -> list:
        data = []
        for key, value in parse_list.items():
            if key != "target":
                data.append(value)
        return data
    
    def fetch_detail(self, id_list: Union[list, str]) -> list:
        if isinstance(id_list, list):
            data = self.find_id_list(id_list=id_list)
        elif isinstance(id_list, str):
            data = []
            detail_list = self.dict_file[id_list[0]][id_list[1:3]]
            for detail in detail_list:
                if detail["number"] == id:
                    data.append(detail)
        return data
    
    def nearest_toilet(self, location: dict, toilet_list: list) -> dict:
        nearest = None
        near_uuid = None
        near_loc = None
        now_lat = float(location["lat"])
        now_lng = float(location["lng"])
        for toilet in toilet_list:
            
            toilet_lat = float(toilet["lat"])
            toilet_lng = float(toilet["lng"])
            center = { "lat": (toilet_lat + now_lat) / 2, "lng": (toilet_lng + now_lng) / 2 }
            distance = geodesic((now_lat, now_lng), (toilet_lat, toilet_lng)).km
            if nearest is None:
                nearest = distance
                near_uuid = toilet["uuid"]
                near_loc = center
            elif nearest > distance:
                nearest = distance
                near_uuid = toilet["uuid"]
                near_loc = center
                
        data = { "nearest_uuid": near_uuid, "distance": nearest, "near_loc": near_loc }

        return data

    def toilet_around_place(self, location: dict) -> list:
        lat = float(location["lat"])
        lng = float(location["lng"])
        return_data = []

        
        if (lat > 27.99 or lat < 20.01) or (lng > 123.99 or lng < 120.01):
            return return_data
        else:
            for control_lng in range(-1, 2):
                temp_lng = lng + control_lng * 0.01
                for control_lat in range(-1, 2):
                    temp_lat = lat + control_lat * 0.01
                    
                    lat_id, lng_id, float_id = id_encoder(number_lat=str(temp_lat),
                                                        number_lng=str(temp_lng))
                    
                    filter_list = self.id_file[str(lng_id)][str(lat_id)][str(float_id)]
                    
                    return_data.append(filter_list)
                    
            return_data = [item for sublist in return_data for item in sublist]
           
        return return_data
    
    def inside_bounds_toilet(self, bounds: dict) -> list:
        latNorth = float(bounds["latNorth"]) 
        latSouth = float(bounds["latSouth"])
        lngWest = float(bounds["lngWest"])
        lngEast = float(bounds["lngEast"])
        data = []
        tra_data = []
        
        if (latNorth > 28 or latSouth < 20) or (lngEast > 124 or lngWest < 117):
            return data
        else:
            for control_lng in np.arange(lngWest, lngEast + 0.01, 0.01):
                for control_lat in np.arange(latSouth, latNorth + 0.01, 0.01):
                    
                    lat_id, lng_id, float_id = id_encoder(number_lat=str(control_lat),
                                                          number_lng=str(control_lng))
                    
                    filter_list = self.id_file[str(lng_id)][str(lat_id)][str(float_id)]
                    
                    data.append(filter_list)
                    
            data = [item for sublist in data for item in sublist]
            data_length = len (data)
            
            if data_length <= 75 or data_length == 0:
                tra_data = data
            else:
                data_diff = math.floor(len(data) / 75)
                for index, _ in enumerate(data):
                    if index % data_diff == 0:
                        tra_data.append(data[index])       
        
        return tra_data
 
    
if __name__ == "__main__":
    
    data = DataFetch(place_path=os.getenv("PLACE_PATH"),
                     sort_path=os.getenv("SORT_PATH"),
                     id_path=os.getenv("ID_PATH"))
    
    catch = data.toilet_around_place(location={ "lat": "24.3", "lng": "121.3"})
    print(catch)