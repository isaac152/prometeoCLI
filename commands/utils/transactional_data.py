#Python imports
import csv
from datetime import datetime
import requests
import copy

#External libraries import
from typing import Optional,List,Dict
import typer
from tabulate import tabulate

#Local imports
from commands.utils.json_file import get_value,set_value
from commands.utils.errors import APIConnectionError 
from commands.utils.colors import coloring_balances, success_message, warning_message,error_message
from commands.utils.pdf import create_pdf
from commands.utils.report import check_file_name

from commands.start import start
from commands.providers import pick_provider
from commands.auth import get_session_key

from config import PROVIDERS_FILE_NAME,URL


DATE_FORMATS = ["%d-%m-%Y",'%Y-%m-%d','%m-%d%-%Y','%m/%d/%Y','%d/%m/%Y','%Y/%m/%d']


def get_provider_code(provider_code:Optional[str]="")->str:
    """Verify, pick and return a bank provider code"""    
    try:
        provider_code=provider_code.strip().lower()
        session = get_value("sessions")
        if(not session):
            warning_message("Please login first")
            start()
            raise typer.Exit()
        actual_providers=[provider for provider in session.keys() if provider.startswith(provider_code)]
        if not actual_providers:
            actual_providers=session.keys()
        if(provider_code not in actual_providers):
            providers_data = [get_value(provider,PROVIDERS_FILE_NAME) for provider in actual_providers]
            title=f"We cant found any code with: '{provider_code}', but select one from this list: "
            provider_code=pick_provider(providers_data,title)['code']   
        return provider_code 
    except Exception as e:
        error_message(e)


def get_data_from_api(endpoint:str,field:str,session_key:str)->List[Dict[str,str]]:
    """Transactional data API call logic. Return the JSON data if the request was ok"""
    try:       
        r= requests.get(URL+endpoint, params={'key':session_key},headers={'X-API-Key':get_value('API_KEY')})
        if r.status_code!=200:
            raise APIConnectionError(r.json().get('message','Something happend. Please Try again'))
        return r.json()[field]
    except Exception as e:
        error_message(e)
        typer.Exit()

def get_movements_from_api(bank_code:str,currency:str,endpoint:str,first_date:datetime,last_date:datetime)->Dict[str,str]:
    """Movements data API call logic. Return the JSON data if the request was ok"""
    try:
        params={
                'key':get_session_key(bank_code),
                'currency':currency,
                'date_start':first_date.strftime('%d/%m/%Y'),
                'date_end':last_date.strftime('%d/%m/%Y')
            }
        r= requests.get(URL+endpoint,params=params,headers={'X-API-Key':get_value('API_KEY')})
        if r.status_code!=200:
            raise APIConnectionError(r.json())
        return r.json()['movements']
    except Exception as e:
        error_message(e)

def comparing_balances(field:str,provider:str,info:List[Dict[str,str]])->List[Dict[str,str]]:
    """
        Check the difference between the info between the last call and the actual call. 
        If the actual balance is more or less, it will return a specific style
    """
    data = get_value(field)
    if(not data or not data[provider]):
        return info
    data_provider = data[provider]
    balances_keys = [balance for balance in data_provider[0].keys() if balance.startswith('balance')]
    data_provider = {data['id']:data for data in data_provider}
    info_color = copy.deepcopy(info)
    for values in info_color:
        for key in balances_keys:
            new_balance= values[key]
            old_balance = data_provider[values['id']][key]
            values[key]= coloring_balances(new_balance,old_balance)
    return info_color

def wrapper_transactional_data(bank:str,endpoint:str,field:str)->None:
    """Execute all the functions related to get transactional data"""
    provider = get_provider_code(bank)
    key = get_session_key(provider)
    info = get_data_from_api(endpoint,field,key)
    info_colors = comparing_balances(field,provider,info)
    typer.echo('\n'+tabulate(info_colors,headers='keys')+'\n')
    set_value(field,{
        provider:info
    })
        


def comparing_dates(start_date:datetime,end_date:datetime)->bool:
    """Compare two dates"""
    return True if start_date<=end_date else False

def format_selector_movements(info:Dict[str,str])->str:
    """Callback to parse the accounts/cards into a string format """
    return f"{info['name']} - {info.get('currency','')}"


def movements_table_format(movements:List[Dict[str,str]])->None:
    """Format the movements data to display a stylish table on console"""

    movements=copy.deepcopy(movements)
    #Delete all keys we wont use
    [ [i.pop('id'),i.pop('reference'),i.pop('extra_data')] for i in movements]

    #Get the total debit,credit and balance
    debit = round(sum([i['debit'] for i in movements if i['debit']]),2)
    credit = round(sum([i['credit'] for i in movements if i['credit']]),2)
    balance=round(credit-debit,2)

    #Format the table and append the new data (totals)
    balance_color = typer.colors.GREEN if balance>0 else typer.colors.RED 
    movements.append({'detail':'Total','debit':debit,'credit':credit})
    movements.append({'detail':'Total Balance','debit':typer.style(balance,fg=balance_color,bold=True)})
    
    #Create and display the table
    table= tabulate(movements,headers={key:key.upper() for key in movements[0].keys()},tablefmt='fancy_grid')
    typer.echo(table)

def saving_csv(filename:str,data:List[Dict[str,str]])->None:
    """ Create a csv with the movements data """
    with open(filename,'w') as csv_file:
        writer = csv.DictWriter(csv_file,fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def saving_pdf(filename:str,data:List[Dict[str,str]],extra_info:Dict[str,str])->None:
    """ Create a PDF with the movements data"""
    texts = [
        extra_info['bank_name'],
        extra_info['operation'],
        f'From {extra_info["start_date"]} To {extra_info["last_date"]}'
    ]
    create_pdf(filename,data,texts)


def wrapper_saving(filename:str,data:List[Dict[str,str]],extra_info:List[Dict[str,str]])->None:
    """Execute the saving function based on the format"""
    filename=filename.lower()
    if(filename.endswith('.csv')):
        saving_csv(filename,data)
    else:
        saving_pdf(filename,data,extra_info)
    success_message(f'The file {filename} was saved')