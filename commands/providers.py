#External libraries import
import typer
import requests
from pick import pick
from tabulate import tabulate

#Python imports
from typing import List, Optional,Dict

#Local imports
from commands.utils.errors import APIConnectionError
from commands.utils.json_file import get_value, save_file
from commands.utils.colors import error_message

from config import PROVIDERS_FILE_NAME, URL


app = typer.Typer(help="Get a list of the bank providers 🗒️")


def get_providers(key:str="")->List[Dict[str,str]]:
    """
        Get the providers from the API
    """
    try:
        key = key or get_value('API_KEY')
        r=requests.get(URL+'provider/',headers={'X-API-KEY':key})
        if r.status_code!=200:
            raise APIConnectionError(r.json()['message'])
        providers = r.json()['providers']
        save_providers_format= {provider['code']:provider for provider in providers}
        save_file(save_providers_format,PROVIDERS_FILE_NAME)
        return providers
    except Exception as e:  
        error_message(e)
        raise typer.Exit()

def format_provider(provider:Dict[str,str])->str:
    """
        Callback to parse the providers into a string format
    """
    return f"{provider.get('country')} -{provider.get('name')}"

def pick_provider(providers:List[str],title:Optional[str]='Please select a bank provider')->Dict[str,str]:
    """
        Use pick library to select the provider
    """
    return pick(providers,title,indicator='=>',options_map_func=format_provider)[0]

def show_providers(country:Optional[str]="")->None:
    """
        Show a list of the banks avaliable on Prometeo.
        The list can be filtered by a country code.
    """
    providers = get_providers()
    country = country.strip().upper()
    if(country):
        providers=[provider for provider in providers if(provider['country']==country)]
    providers = [[provider['name'],provider['code']] for provider in providers]
    providers_tabulate = tabulate(providers,headers=['Bank name','Bank code'],tablefmt="fancy_grid")
    typer.echo(providers_tabulate)


@app.callback(invoke_without_command=True)
def callback(
    country:Optional[str]=typer.Option(
        '',
        '--country','-ct',
        help="Country code to filter the banks"
        )
    )->None:
    show_providers(country)
