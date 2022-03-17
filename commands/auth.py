from typing import Optional
import requests
import typer
from datetime import datetime


from config import URL
from .auxiliar.json_file import get_value,set_value
from commands.auxiliar.errors import APIConnectionError
from commands.auxiliar.colors import success_message,warning_message,error_message

app = typer.Typer(help="Login into your bank account 🏦")


def check_session(provider:str)->bool:
    accounts=get_value('accounts')
    bank_info= accounts.get(provider,None)
    current_time = datetime.now()
    if(bank_info):
        session_time = (current_time-datetime.fromisoformat(bank_info['time'])).total_seconds()/60
        if(session_time<5):
            return True
    return False

def authentication(username:str,password:str,code:str)->None:
    try:
        key = get_value('API_KEY')
        r = requests.post(
            URL+'login/',   
            data={
                    'username':username,
                    'password':password,
                    'provider':code
                },
            headers={'X-API-KEY':key}
            )
        if(r.status_code!=200):
            raise APIConnectionError(r.json().get('message','Cannot login, try again'))
        session_key = r.json()['key']
        set_value('accounts',{
            code:{
                'username':username,
                'password':password,
                'key':session_key,
                'time':str(datetime.now())
        }})
        success_message("Login successful")
    except APIConnectionError as e:  
        error_message(e)
        raise typer.Exit()
    
#Arreglarse si tiene más de una cuenta por banco
def auth_wrapper(username:str,password:str,provider:str)->None:
    if(not check_session(provider)):
        authentication(username,password,provider)
        return
    warning_message("You have an actual session on this bank")

@app.command("login")
def login(
    username:Optional[str]=typer.Option(...,"--user","-u",help="Bank username",prompt="Please write your user"),
    password: Optional[str]=typer.Option(...,"--pass","-p",help="Bank password",prompt="Please write your pass",hide_input=True),
    code : Optional[str]=typer.Option(...,'--code','-c',help="Bank code",prompt="Please write the bank code")
    )->None:
    """
        Login into your bank account. The app will save session data to easy access in other commands.\n
        Note:\n
            Use 'providers get' to see all bank codes on Prometeo
    """
    auth_wrapper(username,password,code)


#Arreglarse si tiene más de una cuenta por banco

@app.command("logout")
def logout(
    bank_code:Optional[str]=typer.Option('',"--code","-c",help="The code of the bank you want to logout"),
    all_flag:Optional[bool]=typer.Option(False,'--all','-a',help="Delete all the session data")
    )->None:
    """
        Logout from your bank account. This will delete all the session data.
    """
    try:
        if not all_flag:
            accounts=get_value('accounts')
            del accounts[bank_code]
            set_value('accounts',accounts)
        else:
            set_value('accounts',{})
        typer.echo("Logout successful")
    except KeyError:
        if bank_code:
            typer.echo("You have not login on any account in this bank")
        else:
            typer.echo('Please specifiy in which bank do you want to logout')
    finally:
        raise typer.Exit()

    