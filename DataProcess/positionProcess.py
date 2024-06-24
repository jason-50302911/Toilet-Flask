import json
import os

from typing import Union
from tqdm.auto import tqdm
from pathlib import Path

def create_empty_dict(input_dict: dict) -> dict:
    for lng_id in range(117, 124, 1):
        input_dict[str(lng_id)] = {}
        
    for lng in input_dict.values():
        for lat_id in range(20, 28):
            lng[str(lat_id)] = {}
    
    for lng_id in input_dict.values():
        for lat_id in lng_id.values():
            for float_id in range(0, 10000):
                lat_id[str(float_id)] = []
    
            
def id_encoder(number_lat: str, number_lng: str) -> int:
    
    lat_identity = number_lat[0:6]
    lng_identity = number_lng[0:7]
    
    lat_id = int(lat_identity[0:2])
    lng_id = int(lng_identity[0:3])
    
    float_id = int(lat_identity[3:5] + lng_identity[4:6])

    return lat_id, lng_id, float_id

def toilet_identify(toilet_type: str) -> Union[str, int]:
    if toilet_type == "親子廁所":
        return 1
    elif toilet_type == "男廁所":
        return 2
    elif toilet_type == "女廁所":
        return 3
    elif toilet_type == "無障礙廁所":
        return 4
    elif toilet_type == "性別友善廁所":
        return 5
    elif toilet_type == "混合廁所":
        return 6
    else:
        return toilet_type


def create_id_data(data: list, sample: dict, index: int, number_check: int) -> int:
    check_flag = False
    
    cut_lat = sample["latitude"][:7]
    cut_lng = sample["longitude"][:8]
    
    toilet_type = toilet_identify(toilet_type=sample["type"])
    
    if isinstance(toilet_type, str):
        raise ValueError(f"Toilet type is not including in identity list: {toilet_type}")
    
    categroy = { "id":sample["number"], "type": toilet_type }
    
    store_block = {
        "uuid": index,
        "categroy": [categroy],
        "lat": cut_lat,
        "lng": cut_lng,
    }
    
    if len(data) == 0:
        data.append(store_block)
        number_check += 1
    else:
        for exist in data:
            if exist["lat"] == cut_lat and exist["lng"] == cut_lng:
                exist["categroy"].append(categroy)
                number_check += 1
                check_flag = True
        if check_flag is False:
            data.append(store_block)
            number_check += 1
    
    return number_check
    


def write_id_list(input_data: list) -> list:
    id_dict = {}
    create_empty_dict(input_dict=id_dict)
    
    number_check = 0

    for index, sample in tqdm(enumerate(input_data)):
        
        lat_id, lng_id, float_id = id_encoder(number_lat=sample["latitude"], 
                                              number_lng=sample["longitude"])

        
        number_check = create_id_data(data=id_dict[str(lng_id)][str(lat_id)][str(float_id)], sample=sample, index=index, number_check=number_check)
        
    print(f"Check Number: {number_check}")
        
    return id_dict

def write_data(input_data: Union[dict, list],
               file_name: str):
    
    write_mode = None
    
    data_path = Path("data/")
    file_path = (data_path / file_name).with_suffix(".json")
    
    if os.path.exists(file_path): 
        file_size = file_path.stat().st_size
        if file_size > 10: 
            print(f"{file_name} file has been writen, skip writing...")
        else: 
            print(f"The {file_name} file is empty, starting writing file...")
            write_mode = True
    else:
        write_mode = True
         
    if write_mode:
        try:
            with open(file_path, mode="w", encoding="utf-8") as file:
                json.dump(input_data, file,  ensure_ascii=False, indent=4)
                print(f"\nCreating data successfully")
        except Exception as error:
            print(f"\nWriting file error: {error}")




if __name__ == "__main__":
    try: 
        with open("data/toilet_data.json", mode="r", encoding="utf-8-sig") as file:
            toilet_data_json = json.load(file)
            
        id_dict = write_id_list(toilet_data_json)
        write_data(input_data=id_dict, file_name="posid")
    except Exception as error:
        print(f"Error message: {error}")

