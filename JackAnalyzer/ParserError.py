from typing import Union, List
from xml.etree.ElementTree import Element

class ParserError(Exception):
    def __init__(self, token: Union[Element, None], message: str, stream: List):
        self.token: Union[Element, None] = token
        self.message: str = message
        self.stream: List = stream
