from typing import List, cast, Callable, Union

from JackAnalyzer.Tokenizer import TokenBuilder, Token, RULES
from JackAnalyzer.Token import KEYWORD_LIST, Node
from JackAnalyzer.Parser import JackParser

sample_let_statements: List[str] = [
    "let s = \"string constant\";",
    "let z = null;",
    "let a[1] = a[2];",
    "let game = SquareGame.new();",
    "let y = y + 2;",
    "let i = i * (-j);",
    "let i = i | j;",
]

def make_tokenstream(line_of_code: str) -> List[Token]:
    tb: TokenBuilder = TokenBuilder(line_of_code, RULES, KEYWORD_LIST)
    tokens: List[Token] = [t for t in tb if t is not None]
    return tokens

def parser_tester(token_stream: List[Token], subparser_name: str) -> Node:
    parser: JackParser = JackParser(token_stream)
    target_method: Callable = getattr(parser, subparser_name)
    result: Node = target_method()
    return result

if __name__ == "__main__":
    # teststr: str = "let game = SquareGame.new();" 
    sample_let: List[str] = [
        "let s = \"string constant\";",
        "let z = null;",
        "let a[1] = a[2];",
        "let game = SquareGame.new();",
        "let y = y + 2;",
        "let i = i * (-j);",
        "let i = i | j;",
    ]
    # sample_do: List[str] = [
    #     # "do Screen.drawRectangle((x + size) - 1, y, x + size, y + size);",
    #     # "do game.run();",
    #     # "do Screen.setColor(false);",
    #     "do Screen.drawRectangle(x, y, x + 1, y + size);",
    # ]

    let_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_let] 
    # do_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_do]

    for ts in let_tokenstreams:
        print(f"working on: {ts}")
        res: Node = parser_tester(ts, "_subroutine_let")
        assert res

    # import pdb
    # pdb.set_trace()
    # for ts in do_tokenstreams:
    #     res = parser_tester(ts, "_subroutine_do")
    #     print(res.xml())
    #     assert res

    print("finished")
