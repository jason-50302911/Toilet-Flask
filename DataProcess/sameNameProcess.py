import json
import itertools

from tqdm.auto import tqdm
from positionProcess import write_data, toilet_identify


def create_small_aggre_data(layer2_data: list, compar_list: list, number_check: int) -> int:
    for sample in layer2_data:
        check_flag = False
        time = None
        
        if len(sample["time"]["星期一"]) == 0 and len(sample["time"]["星期二"]) == 0:
            time = { "星期一": [], "星期二": [], "星期三": [], "星期四": [], "星期五": [], "星期六": [], "星期日": [] }
        else:
            time = sample["time"]
        
        name = None
        keys = sample.keys()    
        if "actname" not in keys:
            name = sample["name"]
        else:
            name = sample["actname"]
            
        store_few_info = {
            "id": sample["number"],
            "name": name,
            "type": toilet_identify(toilet_type=sample["type"]),
            "floor": sample["floor"],
        }
        store_block = {
            "name": sample["name"],
            "address": sample["address"],
            "latitude": sample["latitude"],
            "longitude": sample["longitude"],
            "patterns": sample["patterns"],
            "time": time,
            "spare": sample["spare"],
            "type3": sample["type3"],
            "facilities": sample["facilities"],
            "aggregate": [store_few_info]
        }
        if len(compar_list) == 0: 
            compar_list.append(store_block)
            number_check += 1
        else:
            for comp in compar_list:
                if comp["name"] == sample["name"] or (sample["latitude"] == comp["latitude"] and sample["longitude"] == comp["longitude"]):
                    comp["aggregate"].append(store_few_info)
                    check_flag = True
                    number_check += 1
            if check_flag is False:
                compar_list.append(store_block)
                number_check += 1
                
    return number_check
                
                
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

def create_pos_list(data: dict) -> list:
    compar_list = []
    number_check = 0
    for header_value in tqdm(data.values()):
        for sec_value in header_value.values():
            # breakpoint()
            number_check = create_small_aggre_data(layer2_data=sec_value, compar_list=compar_list, number_check=number_check)

    
    print(number_check)
    
    return compar_list
    

            
            
if __name__ == "__main__":
    try: 
        with open("data/idDict.json", mode="r", encoding="utf-8-sig") as file:
            toilet_data_json = json.load(file)
        pos_list = create_pos_list(data=toilet_data_json)
        write_data(input_data=pos_list, file_name="posList")
    except Exception as error:
        print(f"Error message: {error}")
