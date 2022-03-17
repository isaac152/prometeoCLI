class NotAPIKey(Exception):
    def __str__(self)->str:
        return "The program need an API KEY to continue, please try again"

class APIConnectionError(Exception):
    def __init__(self, message:str) -> None:
        self.message=message
    def __str__(self) -> str:
        return self.message