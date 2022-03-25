#Python imports 
import os
import requests
from typing import List
#Local import
from commands.utils.colors import error_message
from commands.utils.graph import wrapper_graphs
from config import IMAGE_FOLDER 




def check_file_name(filename:str)->bool:
    """Validate the file format"""
    if '.' not in filename:
      return False
    format_name= filename.split('.')[1].upper()
    if(format_name!='PDF' and format_name!='CSV'):
        error_message('We dont support this file format')
        return False
    return True
    
def get_images()->None:
  """Download the Prometeo logo and a content divider"""
  urls = [
        'https://cdn.prometeoapi.com/static/img/primary%402x.png',
        'https://miro.medium.com/max/1400/1*yhG7orf9lABajiMrAfF5WQ.png'
    ]
  
  #Get and save every image
  for i,url in enumerate(urls):
    img_data = requests.get(url).content
    with open(f'{IMAGE_FOLDER}/image{i}.png','wb') as image:
      image.write(img_data)

def wrapper_image(data:List[List[str]])->None:
    """Execute all the images related functions"""
    #Create the folder if not exist 
    if not os.path.exists(IMAGE_FOLDER):
      os.mkdir(IMAGE_FOLDER)

    #Download the Prometeo's images
    get_images()
    
    #Create and save the charts
    wrapper_graphs(data)