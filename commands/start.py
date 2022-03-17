import typer

from commands.auxiliar.json_file import get_value
from commands.auxiliar.colors import error_message
from .providers import get_providers,pick_provider
from .auth import auth_wrapper
from .api_key import save_key

app = typer.Typer(help="This command will initialize your bank data")



def start()->None:
    """
        Exectue in order all the logic to login and start using the app
    """
    try:
        key = get_value('API_KEY')
        if not(key):
            key=save_key(typer.prompt("Please write your API-KEY"))
        providers =get_providers(key)
        provider = pick_provider(providers)[0]
        username = typer.prompt(f"Your username for {provider['name']}")
        password = typer.prompt(f"Your password for {provider['name']}",hide_input=True)
        auth_wrapper(username,password,provider['code'])
    except Exception as e:
        error_message(e)
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def callback():
    start()
