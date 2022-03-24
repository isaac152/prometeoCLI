from typing import Optional
import requests
import typer
from datetime import datetime
from commands.providers import get_providers, pick_provider


from config import URL
from commands.utils.json_file import get_value,set_value
from commands.utils.errors import APIConnectionError, NotAPIKey,TimeOutSession
from commands.utils.colors import success_message,error_message, warning_message

app = typer.Typer(help="Login/logout into your bank account 🏦")

def get_session_key(provider:Optional[str]="")->str:
    """ Get the session key by a specific bank code"""
    try:
        session = get_value('sessions')
        key = auth_wrapper(
            session[provider]['username'],
            session[provider]['password'],
            provider
        )
        return key
    except APIConnectionError as e :
        error_message(e)
        typer.Exit()

def check_session(provider:str)->bool:
    """
        Validate if session is still open and return a boolean based on it. 
        5 minutes per session key.
    """
    try:
        sessions=get_value('sessions')
        bank_info= sessions.get(provider,None)
        current_time = datetime.now()
        if(bank_info):
            session_time = (current_time-datetime.fromisoformat(bank_info['time'])).total_seconds()/60
            if(session_time<5):
                return True
        raise TimeOutSession()
    except Exception as e:
        return False
        #error_message(e)

def authentication(username:str,password:str,code:str)->str:
    """Login API call login. Return the session key"""
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
        set_value('sessions',{
            code:{
                'username':username,
                'password':password,
                'key':session_key,
                'time':str(datetime.now())
        }})
        return session_key
    except APIConnectionError as e:  
        error_message(e)
        raise typer.Exit()
    
def auth_wrapper(username:str,password:str,provider:str)->str:
    """Execute the authentication related functions. Return the session key"""
    if(not check_session(provider)):
        return authentication(username,password,provider)
    provider_info = get_value('sessions').get(provider,None)
    return provider_info['key']
    #warning_message("You have an actual session on this bank")

@app.command("login")
def login(
    username:Optional[str]=typer.Option(...,"--user","-u",help="Bank username",prompt="Please write your user"),
    password: Optional[str]=typer.Option(...,"--pass","-p",help="Bank password",prompt="Please write your pass",hide_input=True),
    code : Optional[str]=typer.Option('','--code','-c',help="Bank code")
    )->None:
    """
        Login into your bank account. The app will save session data to easy access in other commands.\n
        Note:\n
            Use 'providers get' to see all bank codes on Prometeo and have a faster login.
    """
    if not code:
        code  = pick_provider(get_providers())['code']
    auth_wrapper(username,password,code)
    success_message("Login successful")    


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
            sessions=get_value('sessions')
            key= sessions[bank_code]['key']
            r=requests.get(f'{URL}logout/{key}',headers={'X-API-KEY':get_value('API_KEY')})
            del sessions[bank_code]
            if r.status_code!=200:
                raise NotAPIKey
            set_value('sessions',sessions)
        else:
            set_value('sessions',{})
        success_message("Logout successful")
    except (KeyError,NotAPIKey):
        if bank_code:
            warning_message("You have not login on any account in this bank")
        else:
            warning_message('Please specifiy in which bank do you want to logout')
    finally:
        raise typer.Exit()

    