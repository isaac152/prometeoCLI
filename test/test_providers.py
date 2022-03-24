import os
import random
import pytest
from typer.testing import CliRunner

from test import KEY
from commands.providers import app, get_providers
from commands.utils.json_file import set_value
from config import CONFIG_FILE_NAME


runner = CliRunner()

def test_get_providers_app():
    set_value('API_KEY',KEY)
    assert os.path.exists(CONFIG_FILE_NAME)
    result = runner.invoke(app)
    assert result.exit_code==0
    output = result.stdout
    assert 'Test Provider' in output 
    os.remove(CONFIG_FILE_NAME)


def test_get_providers_by_country():
    set_value('API_KEY',KEY)
    assert os.path.exists(CONFIG_FILE_NAME)
    option = [random.choice(['-ct','--country']),'PE']
    result = runner.invoke(app,option)
    assert result.exit_code==0
    assert 'Peru' in result.stdout
    os.remove(CONFIG_FILE_NAME)

def test_get_providers_bad_key():
    with pytest.raises(Exception): 
        provider = get_providers('bad_key')
        assert provider is None
    
