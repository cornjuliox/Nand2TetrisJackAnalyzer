from typing import List
from JackAnalyzer.Token import Token, Node

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_expression_list: List[str] = [
        "x, y, x + 1, y + size"
    ]

    expression_list_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_expression_list]

    for ts in expression_list_tokenstreams:
        print(f"working on expression list -> {ts}")
        res: Node = parser_tester(ts, "expression_list")
        print(res.xml())
        assert res

    print("finished")
