import json

from positionProcess import write_data, id_encoder
from tqdm.auto import tqdm

def create_empty_dict(input_des):
    start_number = ord('A')
    for index in range(0, 26):
        alphabet = start_number + index
        input_des[chr(alphabet)] = {}
        
def check_city_id(check_dict: dict, city_id: str) -> str: 
    exist = False
    for id in check_dict.keys():
        if id == city_id:
            exist = True
            break
    if exist is False:
        check_dict[city_id] = []         
        
def sort_id(input_data: list) -> dict:
    init_dict = {}
    create_empty_dict(init_dict)
    
    for sample in tqdm(input_data):
        key = sample["number"][0]
        
        check_dict = init_dict[key]
        city_id = sample["number"][1:3]
        
        check_city_id(check_dict=check_dict, city_id=city_id)
        
        if "廁所" not in sample["name"]:
            sample["name"] = sample["name"] + "廁所"
        
        init_dict[key][city_id].append(sample)
        
    return init_dict

def put_data(data: list, ref_data: dict) -> dict:
    for sample in tqdm(data):
        key = sample["number"][0]
        city_id = sample["number"][1:3]
        print(len(ref_data[key][city_id]))
        ref_data[key][city_id].append(sample)
        print(len(ref_data[key][city_id]))

if __name__ == "__main__":
    try:
        with open("data/easyToilet.json", mode="r", encoding="utf-8-sig") as file:
            easy_toilet = json.load(file)
        
        with open("data/idDictOK.json", mode="r", encoding="utf-8-sig") as file:
            id_ok = json.load(file)
            
        put_data(data=easy_toilet, ref_data=id_ok)
        write_data(input_data=id_ok, file_name="idDictSuccess")
    except Exception as error:
        print(f"Error message: {error}")