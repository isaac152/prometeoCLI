from typer.testing import CliRunner


from commands.auth import app
from commands.utils.json_file import get_value,set_value
from config import CONFIG_FILE_NAME


runner = CliRunner()

def active_session():
    pass
def inactive_session():
    pass
def bad_login():
    pass
def good_login():
    pass
