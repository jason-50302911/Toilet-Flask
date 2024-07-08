import json

from positionProcess import write_data, id_encoder
from tqdm.auto import tqdm
import itertools 

def obey_data_rule(data: dict) -> dict:
    number = 0
    for header_value in tqdm(data.values()):
        for sec_value in header_value.values():
            for sample in sec_value:
                keys = sample.keys()
                if "actname" not in keys:
                    sample["actname"] = sample["name"]
                
    print(number)
                
def comb_name(data: dict, check_name: list) -> dict:
    number = 0
    number_deal = 0

    for header_value in tqdm(data.values()):
        for sec_value in header_value.values():
            for sample in sec_value:
                number += 1
                
                for ref_sample in check_name:
                    if ref_sample["address"] == sample["address"]:
                        for ref_aggre in ref_sample["aggregate"]:
                            if ref_aggre["id"] == sample["number"]:
                                number_deal += 1
                                sample["name"] = ref_sample["name"]
                                sample["floor"] = ref_aggre["floor"]
    
    print(number, number_deal)
                        
def add_uuid(data: list) -> list:
    uuid = 14299
    for sample in data:
        uuid += 1
        sample["uuid"] = uuid
        
def sort_for_type(name: str) -> str:
    type_name = None
    conv_store = ["統一超商", "全家", "萊爾富", "7-11", "來來", "OK", "超商"]
    gas_sta = ["加油站", "中油", "統一精工"]
    chain_store = ["摩斯", "麥當勞", "星巴克", "家樂福", "全聯", "肯德基", "KFC", "寶雅", "85度", "特力屋", "千葉", "爭鮮", "吉野家"]
    
    if name in conv_store:
        type_name = "便利商店"
    elif name in gas_sta:
        type_name = "加油站"
    elif name in chain_store:
        type_name = "連鎖商店"
    else: 
        type_name = "公廁"
    
    return type_name

def create_sort(data: dict) -> None:
    for header_value in tqdm(data.values()):
        for sec_value in header_value.values():
            for sample in sec_value:
                if sample["type2"] == "一般商家":
                    sample["type3"] = sample["type2"]
                else:
                    type3 = sort_for_type(name=sample["name"])
                    sample["type3"] = type3
        
def grab_type2(data: list) -> list:
    grab_list = []
    
    for header_value in tqdm(data.values()):
        for sec_value in header_value.values():
            for sample in sec_value:
                if len(grab_list) == 0:
                    grab_list.append(sample["type2"])
                else:
                    flag = False
                    for grab in grab_list:
                        if grab == sample["type2"]: flag = True
                
                    if not flag: grab_list.append(sample["type2"])
    
    print(grab_list)
        
def comb_pos(data: list, pos_id: dict):
    for sample in tqdm(data):
        lat_id, lng_id, float_id = id_encoder(number_lat=sample["latitude"], 
                                              number_lng=sample["longitude"])
        pos_inside_list = pos_id[lng_id][lat_id][float_id]
        length = len(pos_inside_list)
        sample['lat'] = sample["latitude"]
        sample['lng'] = sample["longitude"]
        del sample["latitude"]
        del sample["longitude"]
        pos_id[lng_id][lat_id][float_id].append(sample)
        if  len(pos_inside_list) != length + 1: 
            print("Data is failed to insert")
            
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
        with open("data/idDict.json", mode="r", encoding="utf-8-sig") as file:
            id_dict = json.load(file)
    
        # with open("data/checkName.json", mode="r", encoding="utf-8-sig") as file:
        #     check_name = json.load(file)
        
        # check_name = aggre_name(data=id_dict)
        # comb_name(data=id_dict, check_name=check_name)
        # add_uuid(data=easy_list)
        # comb_pos(data=easy_list, pos_id=pos_id)
        # obey_data_rule(data=id_dict)
        # grab_type2(data=id_dict)
        create_sort(data=id_dict)
        write_data(input_data=id_dict, file_name="idDict1")
    except Exception as error:
        print(f"Error message: {error}")