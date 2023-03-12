from typing import List

from JackAnalyzer.Tokenizer import TokenBuilder, Token, RULES
from JackAnalyzer.Token import KEYWORD_LIST, Node
from JackAnalyzer.Parser import JackParser

def make_tokenstream(line_of_code: str) -> List[Token]:
    tb: TokenBuilder = TokenBuilder(line_of_code, RULES, KEYWORD_LIST)
    tokens: List[Token] = [t for t in tb if t is not None]
    return tokens

if __name__ == "__main__":
    teststr: str = "let game = SquareGame.new();" 
    tokens: List[Token] = make_tokenstream(teststr)
    parser: JackParser = JackParser(tokens)
    output: Node = parser._subroutine_let()
    flattened: List[str] = [x for x in output()]
    print(flattened)
    # print(tokens)
