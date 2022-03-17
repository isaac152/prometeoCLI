from typing import List, Optional,Dict
import requests
import typer
from pick import pick
from tabulate import tabulate

from commands.auxiliar.errors import APIConnectionError
from commands.auxiliar.json_file import get_value
from commands.auxiliar.colors import error_message

from config import URL

app = typer.Typer(help="Get a list of the bank providers")


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
        return providers
    except Exception as e:  
        error_message(e)
        raise typer.Exit()

def format_provider(provider:Dict[str,str])->str:
    """
        Callback to parse the providers into a string format
    """
    return f"{provider.get('country')} -{provider.get('name')}"

def pick_provider(providers:List[str])->Dict[str,str]:
    """
        Use pick library to select the provider
    """
    title = 'Please select a bank provider'
    return pick(providers,title,indicator='=>',options_map_func=format_provider)

def show_providers(country:Optional[str]="")->None:
    """
        Show a list of the banks avaliables on Prometeo.
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
