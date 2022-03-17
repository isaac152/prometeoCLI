import json
import os

from typing import Dict
from config import FILE_NAME



def set_value(key:str,value:any)->None:
    config= {}
    if os.path.exists(FILE_NAME):
        config = parse_json() 
    config.update({key:value})
    save_file(config)

def get_value(key:str)->any:
    if not os.path.exists(FILE_NAME):
        return None
    config = parse_json() 
    return config.get(key,None)

def parse_json()->Dict[str,str]:
    with open(FILE_NAME,'r') as json_file:
        config = json.load(json_file)
    return config

def save_file(config:Dict[str,str])->None:
    with open(FILE_NAME,'w') as json_file:
        json.dump(config,json_file,indent=4)