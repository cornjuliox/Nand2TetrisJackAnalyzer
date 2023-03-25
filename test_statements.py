from typing import List
from xml.etree.ElementTree import indent, dump

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
        """
        do Screen.setColor(false);
        do Screen.drawRectangle(x, (y + size) - 1, x + size, y + size);
        let y = y - 2;
        do Screen.setColor(true);
        do Screen.drawRectangle(x, y, x + size, y + 1);
        """,
    ]
    statement_token_list: List[List[Token]] = [make_tokenstream(x) for x in sample_statement_list]

    for ts in statement_token_list:
        print(f"working on expression list -> {ts}")
        res: Node = parser_tester(ts, "statements")
        indent(res)
        dump(res)

        assert res


    print("finished")
