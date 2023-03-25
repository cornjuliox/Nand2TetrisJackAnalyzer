from typing import List
from JackAnalyzer.Token import Token, Node

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_expressions: List[str] = [
        "a + b;",
        "i = i | j;",
    ]

    expression_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_expressions] 

    for ts in expression_tokenstreams:
        print(f"working on: {ts}")
        res: Node = parser_tester(ts, "expression")
        assert res
