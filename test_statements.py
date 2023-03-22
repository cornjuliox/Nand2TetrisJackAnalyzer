from typing import List
from JackAnalyzer.Token import Token, Node

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_statement_list: List[str] = [
        """
        let x = Ax;
        let y = Ay;
        let size = Asize;
        do draw();
        """,
        """
        do erase();
        let size = size + 2;
        do draw();
        """,
    ]
    statement_token_list: List[List[Token]] = [make_tokenstream(x) for x in sample_statement_list]

    for ts in statement_token_list:
        print(f"working on expression list -> {ts}")
        import pdb
        pdb.set_trace()
        res: Node = parser_tester(ts, "statements")
        assert res

    print("finished")
