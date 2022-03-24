#External libraries import
import typer

def success_message(message:str)->None:
    """Create a green message in the console"""
    typer.echo(typer.style(message, fg=typer.colors.GREEN, bold=True))
    
def error_message(message:str)->None:
    """Create a red message in the console"""
    typer.echo(typer.style(message, fg=typer.colors.RED, bold=True))

def warning_message(message:str)->None:
    """Create a yellow message in the console"""
    typer.echo(typer.style(message, fg=typer.colors.YELLOW, bold=True))

def coloring_balances(new_balance:int,old_balance:int)->typer.style:
    """Return a specific color and style based on two numbers"""
    if(new_balance>old_balance):
        return typer.style(new_balance, fg=typer.colors.BRIGHT_GREEN,bold=True)
    elif(new_balance==old_balance):
        return typer.style(new_balance, fg=typer.colors.GREEN,bold=True)
    return typer.style(new_balance, fg=typer.colors.RED,bold=True)