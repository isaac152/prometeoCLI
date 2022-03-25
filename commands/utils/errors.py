class NotAPIKey(Exception):
    def __str__(self)->str:
        return "The program need an API KEY to continue, please try again"

class APIConnectionError(Exception):
    def __init__(self, message:str) -> None:
        self.message=message
    def __str__(self) -> str:
        return self.message

class TimeOutSession(Exception):
    def __str__(self)->str:
        return "Your session is over"

class NotTransactionalSession(Exception):
    def __init__(self,field:str)->None:
        self.field=field
    def __str__(self)->str:
        return f"You need to use the {self.field} at least one time before using movements"