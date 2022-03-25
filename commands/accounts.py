#External libraries
import typer
from pick import pick

#Python imports
from typing import Optional
from datetime import datetime

#Local imports
from commands.utils.colors import error_message, warning_message
from commands.utils.errors import NotTransactionalSession
from commands.utils.json_file import get_value

from commands.utils.transactional_data import DATE_FORMATS, check_file_name, movements_table_format, comparing_dates,format_selector_movements,wrapper_saving
from commands.utils.transactional_data import get_movements_from_api, get_provider_code, wrapper_transactional_data

from config import PROVIDERS_FILE_NAME

app = typer.Typer(help="Info of your bank accounts 💵")

@app.command('movements')
def movements(
    bank:Optional[str]=typer.Option('','-b','--bank',help="The code of your bank"),
    first_date:datetime=typer.Argument(...,formats=DATE_FORMATS,help="First date"),
    last_date:datetime=typer.Argument(datetime.now(),formats=DATE_FORMATS,help="Last date"),
    filename:Optional[str]=typer.Option('','-f','--filename',help="Output filename"),
    count: Optional[int]=typer.Option(0,'-c','--count',help="Max movements to show"),
    reverse:Optional[bool]=typer.Option(False,'-o','--order',help="Reverse chronological order.")
    )->None:
    """
        Get a list of the movements of your account between two dates.\n

        Note: Please use accounts at least one time before using this command. 
    """
    try:
        if(comparing_dates(first_date,last_date)):
            bank = get_provider_code(bank)
            accounts = get_value('accounts')
            if not accounts:
                raise NotTransactionalSession('accounts')
            provider_accounts=accounts[bank]
            result = pick(provider_accounts,options_map_func=format_selector_movements)[0]
            movements = get_movements_from_api(
                bank,
                result['currency'],
                f'account/{result["number"]}/movement/',
                first_date,
                last_date
                )
            movements= movements if not reverse else movements[::-1]
            movements= movements[:count] if count>0 else movements
            movements_table_format(movements)
            if (filename and check_file_name(filename)):
                extra_info={
                    'operation':f'{result["name"]} Movements in {result["currency"]}',
                    'start_date':first_date,
                    'last_date':last_date,
                    'bank_name':get_value(bank,PROVIDERS_FILE_NAME)['name']
                }
                wrapper_saving(filename,movements,extra_info)
                
        else:
            warning_message('Last date must be more recent that the first date')
    except Exception as e:
        error_message(e)
        typer.Exit()

@app.callback(invoke_without_command=True,help="Get info of your bank accounts")
def accounts(
    ctx: typer.Context,
    bank:Optional[str]=typer.Option('','-b','--bank',help="The code of your bank")
)->None:
    try:
        if ctx.invoked_subcommand is None:
            wrapper_transactional_data(bank,'account/','accounts')
    except Exception as e:
        error_message('Please try to use the command again')
