from typing import List
from JackAnalyzer.Token import Token, Node

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_if: list[str] = [
        """
        if (((y + size) < 254) & ((x + size) < 510)) {
            do erase();
            let size = size + 2;
            do draw();
        }
        """,
        # """
        # if (size > 2) {
        #     do erase();
        #     let size = size - 2;
        #     do draw();
        # }
        # """
    ]

    if_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_if] 

    for ts in if_tokenstreams:
        print(f"working on: {ts}")
        res: Node = parser_tester(ts, "_subroutine_if", debug=True)
        print(res._children)
        assert res

    print("finished")
