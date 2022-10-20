class BasicParserException(Exception):
    """Base class for all parser errors"""

    def __str__(self):
        return "Something goes wrong with parser"


class InvalidUrlError(BasicParserException):
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return f"{self.url} is invalid!"

