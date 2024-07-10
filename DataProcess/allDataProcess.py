import json

from positionProcess import write_data, id_encoder
from tqdm.auto import tqdm
import itertools 

def obey_data_rule(data: list) -> list:
    number = 0
    return_list = []
    
    for sample in tqdm(data):
        city = create_city(address=sample["address"])
        if city is not None: 
            number += 1
            sample["actname"] = sample["name"]
            sample["type2"] = "餐廳"
            sample["grade"] = "優等級"
            sample["spare"] = []
            sample["time"] = {
                    "星期一": [],
                    "星期二": [],
                    "星期三": [],
                    "星期四": [],
                    "星期五": [],
                    "星期六": [],
                    "星期日": []
                },
            sample["administration"] = "商家"
            sample["floor"] = "1F"
            sample["type"] = "混合廁所"
            sample["type3"] = "一般商家"
            sample["facilities"] = []
            sample["city"] = city
            
            return_list.append(sample)
                         
    print(number)
    return return_list
    
def create_city(address: str) -> str:
    return_string = ""
    check = False
    
    if "區" not in address:
        return None 
    else:
        for char in address[3:]:
            if char == "區":
                return_string += char
                check = True
            elif check is False:
                return_string += char
                
        return return_string
                
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
    type_number = None
    conv_store = ["統一超商", "全家", "萊爾富", "7-11", "來來", "OK", "超商"]
    gas_sta = ["加油站", "中油", "統一精工"]
    chain_store = ["摩斯", "麥當勞", "星巴克", "家樂福", "全聯", "肯德基", "KFC", "寶雅", "85度", "特力屋", "千葉", "爭鮮", "吉野家", "路易．莎咖啡"]
    
    for conv in conv_store:
        if conv in name: type_number = 1
    
    for gas in gas_sta:
        if gas in name: type_number = 2
    
    for chain in chain_store:
        if chain in name: type_number = 3
    
    
    if type_number == 1:
        type_name = "便利商店"
    elif type_number == 2:
        type_name = "加油站"
    elif type_number == 3:
        type_name = "連鎖商店"
    else: 
        type_name = "公廁"
    
    return type_name

def create_sort(data: dict) -> None:
    for header_value in tqdm(data.values()):
        for sec_value in header_value.values():
            for sample in sec_value:
                if sample["type2"] == "一般商家" or sample["type2"] == "連鎖商家":
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
        with open("data/borrowData.json", mode="r", encoding="utf-8-sig") as file:
            id_dict = json.load(file)
    
        # with open("data/checkName.json", mode="r", encoding="utf-8-sig") as file:
        #     check_name = json.load(file)
        
        # check_name = aggre_name(data=id_dict)
        # comb_name(data=id_dict, check_name=check_name)
        # add_uuid(data=easy_list)
        # comb_pos(data=easy_list, pos_id=pos_id)
        return_data = obey_data_rule(data=id_dict)
        # grab_type2(data=id_dict)
        # create_sort(data=id_dict)
        write_data(input_data=return_data, file_name="borrowData1")
    except Exception as error:
        print(f"Error message: {error}")