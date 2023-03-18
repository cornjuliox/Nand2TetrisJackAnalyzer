from typing import List, Callable

from JackAnalyzer.Token import Token, Node, KEYWORD_LIST
from JackAnalyzer.Tokenizer import TokenBuilder, RULES
from JackAnalyzer.Parser import JackParser

def make_tokenstream(line_of_code: str) -> List[Token]:
    tb: TokenBuilder = TokenBuilder(line_of_code, RULES, KEYWORD_LIST)
    tokens: List[Token] = [t for t in tb if t is not None]
    return tokens

def parser_tester(token_stream: List[Token], subparser_name: str) -> Node:
    parser: JackParser = JackParser(token_stream)
    target_method: Callable = getattr(parser, subparser_name)
    result: Node = target_method()
    return result
