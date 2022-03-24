#Python imports
import os
import shutil

#External libraries import
import typer

#Local imports
from commands.utils.colors import success_message, warning_message
from config import FOLDER_NAME

app=  typer.Typer(help="This command will delete all the Prometeo saved data 🗑️")


@app.callback(invoke_without_command=True)
def reset()->None:
    if not os.path.exists(FOLDER_NAME):
        warning_message("You don't  have any data on this computer")
        raise typer.Exit()
    shutil.rmtree(FOLDER_NAME,ignore_errors=True)
    success_message("Thanks for using our app")