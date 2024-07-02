import json

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


def create_aggre_data(data: dict) -> dict:
    compar_list = []
    for layer_1 in tqdm(data.values()):
        for layer_2 in layer_1.values():
            create_small_aggre_data(layer2_data=layer_2, compar_list=compar_list)
            
    return compar_list
            
if __name__ == "__main__":
    try: 
        with open("data/idDict.json", mode="r", encoding="utf-8-sig") as file:
            toilet_data_json = json.load(file)
        same_name = create_aggre_data(data=toilet_data_json)
        write_data(input_data=same_name, file_name="name")
    except Exception as error:
        print(f"Error message: {error}")
