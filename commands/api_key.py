import typer
from commands.auxiliar.json_file import set_value,get_value
from commands.auxiliar.errors import NotAPIKey
from commands.auxiliar.colors import success_message,error_message, warning_message


app = typer.Typer(help="Get or set your Prometeo API KEY 🔥")

def save_key(key:str):
    try:
        if(key.strip()):
            set_value('API_KEY',key)
            return key
        raise NotAPIKey()
    except (NotAPIKey,AttributeError) as e:
        error_message(NotAPIKey())
        raise typer.Exit()


@app.command("set")
def insert_key(key:str=typer.Option(
        ...,
        "-k","--key",
        help="Your Prometeo API KEY",prompt='Please write the API-KEY')
        )->None:
    """
        Set and save the key. Required to continue 
    """
    save_key(key)
    success_message("Key setted successfully")



@app.command("get")
def get_key()->None:
    """
        Get the key
    """
    key = get_value('API_KEY')
    if not key:
        warning_message('There is no any API key in this computer, please set one')
        return
    typer.echo(f'Your API-KEY is : {key}')

if __name__=="__main__":
    app()