import json
import itertools

from tqdm.auto import tqdm
from positionProcess import write_data, check_vertical_relation


def create_small_aggre_data(layer2_data: list, compar_list: list):
    for sample in layer2_data:
        check_flag = False
        store_few_info = {
            "id": sample["number"],
            "name": sample["name"],
            "type": sample["type"],
            "floor": check_vertical_relation(sample=sample["name"])
        }
        store_block = {
            "address": sample["address"],
            "type": sample["type"],
            "lat": sample["latitude"],
            "lng": sample["longitude"],
            "aggregate": [store_few_info]
        }
        if len(compar_list) == 0: 
            compar_list.append(store_block)
        else:
            for comp in compar_list:
                if comp["address"] == sample["address"]:
                    comp["aggregate"].append(store_few_info)
                    check_flag = True
            if check_flag is False:
                compar_list.append(store_block)
                
                
def sep_aggre_list(data: list):
    sep_data = []
    
    for sample in tqdm(data):
        check_flag = False
        for aggre in sample["aggregate"]:
            if sample["name"] not in aggre["name"]: 
                check_flag = True
            
        if check_flag:
            sep_data.append(sample)
            
    
    return sep_data
    
    
def aggre_name(data: list) -> list:
    compar_list = []
    for sample in tqdm(data):
        # breakpoint()
        if len(compar_list) == 0:
            compar_list.append(sample)
        else:
            check_flag = False
            for com_sample in compar_list:
                if com_sample["name"] == sample["name"]:
                    com_sample["aggregate"] = list(itertools.chain(com_sample["aggregate"], sample["aggregate"]))
                    check_flag = True    
            if check_flag is False: compar_list.append(sample)
        
    return compar_list
            
            
if __name__ == "__main__":
    try: 
        with open("data/name.json", mode="r", encoding="utf-8-sig") as file:
            toilet_data_json = json.load(file)
        same_name = aggre_name(data=toilet_data_json)
        write_data(input_data=same_name, file_name="name1")
    except Exception as error:
        print(f"Error message: {error}")
