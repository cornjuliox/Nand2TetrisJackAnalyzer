from typing import List
from JackAnalyzer.Token import Token, Node

from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_do: list[str] = [
        "do screen.drawrectangle((x + size) - 1, y, x + size, y + size);",
        "do game.run();",
        "do screen.setcolor(false);",
        "do screen.drawrectangle(x, y, x + 1, y + size);",
    ]
    do_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_do]

    for ts in do_tokenstreams:
        res = parser_tester(ts, "_subroutine_do")
        print(res.xml())
        assert res
    print("finished")
