from typing import List
from xml.etree.ElementTree import indent, dump

from JackAnalyzer.Token import Token, Node
from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_let: list[str] = [
        "let s = \"string constant\";",
        "let z = null;",
        "let a[1] = a[2];",
        "let game = squaregame.new();",
        "let y = y + 2;",
        "let i = i * (-j);",
        "let i = i | j;",
    ]

    let_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_let] 

    for ts in let_tokenstreams:
        print(f"working on: {ts}")
        res: Node = parser_tester(ts, "_subroutine_let")
        indent(res)
        dump(res)
        assert res

    print("finished")
