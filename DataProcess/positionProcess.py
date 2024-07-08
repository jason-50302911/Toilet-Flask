import json
import os

from typing import Union
from tqdm.auto import tqdm
from pathlib import Path

NUMBER_TRANSLATE = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十":10}

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

    return str(lat_id), str(lng_id), str(float_id)

def toilet_identify(toilet_type: str) -> Union[str, int]:
    if toilet_type == "親子廁所":
        return 3
    elif toilet_type == "男廁所":
        return 1
    elif toilet_type == "女廁所":
        return 2
    elif toilet_type == "無障礙廁所":
        return 4
    elif toilet_type == "性別友善廁所":
        return 5
    elif toilet_type == "混合廁所":
        return 6
    else:
        return toilet_type
    
def check_vertical_relation(sample: str) -> str:
    parse_word = None
    for index, word in enumerate(sample):
        if word == "樓":
            if sample[index-1].isdigit():
                parse_word = sample[index-1] + "F"
            elif sample[index-1] in NUMBER_TRANSLATE.keys():
                parse_word = str(NUMBER_TRANSLATE[sample[index-1]]) + "F"
        elif word == "B":
            if len(sample) > index + 1:
                parse_word = word + sample[index+1]
        elif word == "F":
            parse_word = sample[index-1] + word
            
    if "地下" in sample:
        parse_word = "B1"
        
    if parse_word == None:
        parse_word = "1F"
        
    return parse_word

# def check_same_char(str1: str, str2: str) ->str:
#     return_name = ''
#     punc = string.punctuation
#     build_name = "樓棟館"
#     str1_len = len(str1)
#     str2_len = len(str2)
    
#     length = str1_len if str1_len < str2_len else str2_len
    
#     for index in range(length-1):
#         if str1[index] == str2[index] and not str1[index] in punc:
#             if not str1[index] in build_name:
#                 return_name = return_name + str1[index]
            
#     return return_name

def replacement(info: dict):
    name = None
    man = "男廁廁所"
    woman = "女廁廁所"

    if man in info["name"]:
        name = info["name"].replace(man, "")
    elif woman in info["name"]:
        name = info["name"].replace(woman, "")
    else:
        name = info["name"].replace(info["type"], "")

    if info["floor"] in name:
        name = info["name"].replace(info["floor"], "")
        
    return name

# def create_real_name(data: list):
#     ref_name = None

#     ref_name = replacement(info=data[0])

#     for info in data:
#         target_name = replacement(info=info)
#         ref_name = check_same_char(str1=ref_name, str2=target_name)
        
#     return ref_name
            

def create_floor_list(data: list):
    floor_list = []
    for aggre_place in data:
        if aggre_place["floor"] not in floor_list:
            floor_list.append(aggre_place["floor"])
    
    return floor_list    

def create_id_data(data: list, sample: dict, index: int, number_check: int) -> int:
    
    cut_lat = sample["latitude"][:7]
    cut_lng = sample["longitude"][:9]
    
    store_block = {
        "uuid": index,
        "name": sample["name"],
        "address": sample["address"],
        "lat": cut_lat,
        "lng": cut_lng,
        "patterns": sample["patterns"],
        "time": sample["time"],
        "floorList": create_floor_list(data=sample["aggregate"]),
        "aggregate": sample["aggregate"]
    }
    
    data.append(store_block)
    number_check += len(sample["aggregate"])

    return number_check

# def write_name_list(input_data: list) -> list:
#     id_list = []
    
#     number_check = 0

#     for index, sample in tqdm(enumerate(input_data)):
        
#         number_check = create_id_data(data=id_list, sample=sample, index=index, number_check=number_check)
        
#     print(f"Check Number: {number_check}")
    
#     return id_list



def write_pos_dict(input_data: list) -> dict:
    id_dict = {}
    create_empty_dict(input_dict=id_dict)
    
    number_check = 0

    for index, sample in tqdm(enumerate(input_data)):
        lat_id, lng_id, float_id = id_encoder(number_lat=sample["latitude"], 
                                              number_lng=sample["longitude"])
        
        # id_dict[lng_id][lat_id][float_id].append(sample)
        number_check = create_id_data(data=id_dict[lng_id][lat_id][float_id], sample=sample, index=index, number_check=number_check)
        
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
            print(f"{file_name} file has been writen, deleting context and start writing...")
            write_mode = True
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
        with open("data/posList.json", mode="r", encoding="utf-8-sig") as file:
            id_dict = json.load(file)
        
        pos_dict = write_pos_dict(input_data=id_dict)
        write_data(input_data=pos_dict, file_name="posId")
    except Exception as error:
        print(f"Error message: {error}")
