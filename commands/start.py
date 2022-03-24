#External libraries import
import typer

#Local imports
from commands.utils.json_file import get_value
from commands.utils.colors import error_message,success_message

from commands.providers import get_providers,pick_provider
from commands.auth import auth_wrapper
from commands.api_key import save_key


app = typer.Typer(help="This command will initialize your bank data ⭐")



def start()->None:
    """
        Execute in order all the logic to start using the app.
    """
    try:
        #Get the api key, if not exist it will ask the user for it
        key = get_value('API_KEY')
        if not(key):
            key=save_key(typer.prompt("Please write your API-KEY",hide_input=True))
        
        #Get and pick the providers
        providers =get_providers(key)
        provider = pick_provider(providers)

        #User and password prompts
        username = typer.prompt(f"Your username for {provider['name']}")
        password = typer.prompt(f"Your password for {provider['name']}",hide_input=True)
        
        #Validate the login
        auth_wrapper(username,password,provider['code'])
        
        success_message("Login successful")
    except Exception as e:
        error_message(e)
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def callback():
    start()
