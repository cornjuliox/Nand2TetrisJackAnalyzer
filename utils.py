import sys
from typing import List, Callable
from xml.etree.ElementTree import ElementTree

from JackAnalyzer.Token import Token, Node, KEYWORD_LIST
from JackAnalyzer.Tokenizer import TokenBuilder, RULES
from JackAnalyzer.Parser import JackParser

def make_tokenstream(line_of_code: str) -> List[Token]:
    tb: TokenBuilder = TokenBuilder(line_of_code, RULES, KEYWORD_LIST)
    tokens: List[Token] = [t for t in tb if t is not None]
    return tokens

def parser_tester(token_stream: List[Token], subparser_name: str, debug: bool = False) -> Node:
    if debug:
        import pdb
        pdb.set_trace()
    parser: JackParser = JackParser(token_stream)
    target_method: Callable = getattr(parser, subparser_name)
    result: Node = target_method()
    return result

# NOTE: this is an "overridden" version of the dump() function
#       the big change is that it sets short_empty_elements to False
#       so the output matches the XML answer key provided by the class
def dump(elem):
    """Write element tree or element structure to sys.stdout.

    This function should be used for debugging only.

    *elem* is either an ElementTree, or a single Element.  The exact output
    format is implementation dependent.  In this version, it's written as an
    ordinary XML file.

    """
    # debugging
    if not isinstance(elem, ElementTree):
        elem = ElementTree(elem)
    elem.write(sys.stdout, encoding="unicode", short_empty_elements=False)
    tail = elem.getroot().tail
    if not tail or tail[-1] != "\n":
        sys.stdout.write("\n")
