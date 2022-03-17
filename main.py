from typer import Typer
from commands import api_key,providers,auth,start


app = Typer()
app.add_typer(api_key.app,name ="api-key")
app.add_typer(providers.app, name = "providers")
app.add_typer(auth.app, name = "auth")
app.add_typer(start.app,name="init")


if __name__ == '__main__':
    app()