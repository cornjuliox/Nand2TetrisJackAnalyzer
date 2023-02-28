from JackAnalyzer.Token import Token

class ParserError(Exception):
    def __init__(self, token: Token, message: str):
        self.token: Token = token
        self.message: str = message

# NOTE: Don't worry if this doesn't make sense
#       I don't know what I'm doing so I can't explain
#       it to you. 
class KeepGoingError(Exception):
    pass
