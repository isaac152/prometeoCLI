#Python imports
import json
import os
from typing import Dict, Optional

#Local import
from config import CONFIG_FILE_NAME, FOLDER_NAME

""" Each function in this file will have the config file as a default parameter"""


def set_value(key:str,value:any,filename:Optional[str]=CONFIG_FILE_NAME)->None:
    """Update a value of an existing Dict"""
    config= {}
    if os.path.exists(filename):
        config = parse_json(filename) 
    config.update({key:value})
    save_file(config)

def get_value(key:str,filename:Optional[str]=CONFIG_FILE_NAME)->any:
    """Read a JSON file and return only a specific value. The return can be a str, Dict or a List"""
    if not os.path.exists(filename):
        return None
    config = parse_json(filename) 
    return config.get(key,None)

def parse_json(filename:Optional[str]=CONFIG_FILE_NAME)->Dict[str,str]:
    """Load the data from a JSON FILE and return it in a Dict"""
    with open(filename,'r') as json_file:
        config = json.load(json_file)
    return config

def save_file(config:Dict[str,str],filename:Optional[str]=CONFIG_FILE_NAME)->None:
    """Save (and create if doesn't exist) a JSON file with the info of a dict"""
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    with open(filename,'w',encoding='utf-8') as json_file:
        json.dump(config,json_file,indent=4,ensure_ascii=False)