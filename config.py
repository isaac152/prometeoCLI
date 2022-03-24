#Python imports
from pathlib import Path

#Configuration constants
FOLDER_NAME = str(Path.home())+'/.prometeo'
IMAGE_FOLDER = './.images'
CONFIG_FILE_NAME = FOLDER_NAME+'/config.json'
PROVIDERS_FILE_NAME=FOLDER_NAME+'/providers.json'
URL = 'https://banking.sandbox.prometeoapi.com/'