#External libraries import 
from typer import Typer, echo
#Local imports
from commands import accounts, api_key,providers,auth,start,reset,credit_cards

__version__='1.0.0'
#Start point of the app

app = Typer(add_completion=False)
app.add_typer(api_key.app,name ="api-key")
app.add_typer(providers.app, name = "providers")
app.add_typer(auth.app, name = "auth")
app.add_typer(start.app,name="init")
app.add_typer(accounts.app,name="accounts")
app.add_typer(credit_cards.app,name="cards")
app.add_typer(reset.app,name="uninstall")


@app.command('version')
def version():
    echo(__version__)