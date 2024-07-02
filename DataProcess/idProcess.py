import json

from positionProcess import write_data
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

if __name__ == "__main__":
    try:
        with open("data/toilet_data.json", mode="r", encoding="utf-8-sig") as file:
            toilet_data_json = json.load(file)
        id_dict = sort_id(input_data=toilet_data_json)
        for country, city in id_dict.items():
            print(country, len(city))
        write_data(input_data=id_dict, file_name="idDict")
    except Exception as error:
        print(f"Error message: {error}")