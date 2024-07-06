import json

from positionProcess import write_data
from tqdm.auto import tqdm


def produce_id_list(data: dict): 
    number_id_dict = {}
    
    for id_header, header_value in tqdm(data.items()):
        for sec_number, sec_value in header_value.items():
            ins_data = sec_value[0]
            key_name = ins_data["country"] + ins_data["city"]
            value_name = id_header + sec_number + "R"
            
            number_id_dict[key_name] = value_name
            
    print(len(number_id_dict.keys()))

    return number_id_dict

def add_number(data: dict, ref_dict: dict):
    count_dict = {}        

    for sample in tqdm(data):
        place_name = sample["country"] + sample["city"]
        id = ref_dict[place_name]
        keys = count_dict.keys()
        sample_keys = sample.keys()
        
        if "facilities" not in sample_keys: sample["facilities"] = []
            
        if "spare" not in sample_keys: sample["facilites"] = []

        if id not in keys:
            count_dict[id] = 1
            sample_id = "1"
            sample_id = id + sample_id.zfill(6)
            sample["number"] = sample_id
        else: 
            count_dict[id] += 1
            sample_id = str(count_dict[id])
            sample_id = id + sample_id.zfill(6)
            sample["number"] = sample_id         
    
    print(count_dict)



if __name__ == "__main__":
    try:
        with open("data/easyToiletData.json", mode="r", encoding="utf-8-sig") as file:
            easy_dict = json.load(file)
        with open("data/numberId.json", mode="r", encoding="utf-8-sig") as file:
            ref_dict= json.load(file)
        add_number(data=easy_dict, ref_dict=ref_dict)
        write_data(input_data=easy_dict, file_name="easyToilet")
    except Exception as error:
        print(f"Error message: {error}")