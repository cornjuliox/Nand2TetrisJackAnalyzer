from typing import List
from xml.etree.ElementTree import indent

from JackAnalyzer.Token import Token, Node
from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_while: list[str] = [
        """
        while (key = 0) {
            let key = Keyboard.keyPressed();
            do moveSquare();
        }
        """,
    ]

    while_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_while] 

    for ts in while_tokenstreams:
        print(f"working on: {ts}")
        res: Node = parser_tester(ts, "_subroutine_while")
        indent(res)
        dump(res)
        assert res

    print("finished")

