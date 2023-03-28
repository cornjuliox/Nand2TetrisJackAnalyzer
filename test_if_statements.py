from typing import List
from xml.etree.ElementTree import indent

from JackAnalyzer.Token import Token, Node
from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_if: list[str] = [
        # """
        # if (((y + size) < 254) & ((x + size) < 510)) {
        #     do erase();
        #     let size = size + 2;
        #     do draw();
        # }
        # """,
        """
        if (false) {
            let s = "string constant";
            let s = null;
            let a[1] = a[2];
        }
        else {              // There is no else keyword in the Square files.
            let i = i * (-j);
            let j = j / (-2);   // note: unary negate constant 2
            let i = i | j;
        }
        """
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
        res: Node = parser_tester(ts, "_subroutine_if")
        indent(res)
        dump(res)
        assert res

    print("finished")
