import os
import random
from typer.testing import CliRunner


from commands.api_key import app,save_key
from commands.utils.json_file import get_value,set_value
from config import CONFIG_FILE_NAME


runner = CliRunner()

def test_save_key():
    key= 'test'
    save_key(key)
    assert get_value('API_KEY') ==key
    assert os.path.exists(CONFIG_FILE_NAME)
    os.remove(CONFIG_FILE_NAME)



def test_insert_key_by_option():
    options = [
        ["-k","TEST"],
        ['--key',"API_TEST"],
    ]
    option = ['set']+random.choice(options)
    result = runner.invoke(app,option)
    assert result.exit_code == 0
    assert "Key setted successfully\n" in result.stdout
    assert os.path.exists(CONFIG_FILE_NAME)
    os.remove(CONFIG_FILE_NAME)


def test_insert_by_prompt():
    result = runner.invoke(app,['set'],input="TEST\n")
    assert result.exit_code == 0
    assert "Key setted successfully" in result.stdout
    assert os.path.exists(CONFIG_FILE_NAME)
    os.remove(CONFIG_FILE_NAME)


def test_get_key_found():
    key='TEST'
    set_value('API_KEY',key)
    assert os.path.exists(CONFIG_FILE_NAME)
    result = runner.invoke(app,['get'])
    assert result.exit_code == 0
    assert f'Your API-KEY is : {key}' in result.stdout
    os.remove(CONFIG_FILE_NAME)


def test_get_key_not_found():
    result = runner.invoke(app,['get'])
    assert result.exit_code==0
    assert 'There is no any API key on this computer, please set one' in result.stdout
