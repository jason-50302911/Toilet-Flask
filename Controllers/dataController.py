import os

from Controllers.readDataController import read_json
from dotenv import load_dotenv
from DataProcess.positionProcess import id_encoder
from typing import Union

class DataFetch:
    def __init__(self, place_path, sort_path, id_path):
        self.place_path = place_path
        self.sort_file = read_json(sort_path)
        self.id_file = read_json(id_path)
    
    def find_id_list(self, id_list: list[str]) -> list:
        data = []
        for id in id_list: 
            detail_list = self.sort_file[id[0]][id[1:3]]
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
            detail_list = self.sort_file[id_list[0]][id_list[1:3]]
            for detail in detail_list:
                if detail["number"] == id:
                    data.append(detail)
        return data
    

    def toilet_around_place(self, location: dict):
        lat = float(location["lat"])
        lng = float(location["lng"])
        return_data = []
        
        if (lat > 27.99 or lat < 20.01) or (lng > 123.99 or lng < 120.01):
            return return_data
        else:
            for control_lng in range(-1, 3):
                temp_lng = lng + control_lng * 0.01
                for control_lat in range(-1, 2):
                    temp_lat = lat + control_lat * 0.01
                    
                    lat_id, lng_id, float_id = id_encoder(number_lat=str(temp_lat),
                                                        number_lng=str(temp_lng))
                    
                    filter_list = self.id_file[str(lng_id)][str(lat_id)][str(float_id)]

                    return_data.append(filter_list)
                    
            return_data = [item for sublist in return_data for item in sublist]
           
        return return_data
    
if __name__ == "__main__":
    
    load_dotenv()
    
    data = DataFetch(place_path=os.getenv("PLACE_PATH"),
                     sort_path=os.getenv("SORT_PATH"),
                     id_path=os.getenv("ID_PATH"))
    
    catch = data.toilet_around_place(location={ "lat": "24.3", "lng": "121.3"})
    print(catch)