import typer

def success_message(message:str)->None:
    typer.echo(typer.style(message, fg=typer.colors.GREEN, bold=True))
    
def error_message(message:str)->None:
    typer.echo(typer.style(message, fg=typer.colors.RED, bold=True))

def warning_message(message:str)->None:
    typer.echo(typer.style(message, fg=typer.colors.YELLOW, bold=True))