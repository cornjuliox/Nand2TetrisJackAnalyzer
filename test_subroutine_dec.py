from typing import List
from xml.etree.ElementTree import indent

from JackAnalyzer.Token import Token, Node
from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_subroutine_dec: list[str] = [
        # """ 
        # method void moveSquare() {
        #     if (direction = 1) { do square.moveUp(); }
        #     if (direction = 2) { do square.moveDown(); }
        #     if (direction = 3) { do square.moveLeft(); }
        #     if (direction = 4) { do square.moveRight(); }
        #     do Sys.wait(5);  // delays the next movement
        #     return;
        # }
        # """,
        # """
        # method void dispose() {
        #     do square.dispose();
        #     do Memory.deAlloc(this);
        #     return;
        # }
        # """,
        # """
        # function void main() {
        #     var SquareGame game;
        #     let game = SquareGame.new();
        #     do game.run();
        #     do game.dispose();
        #     return;
        # }
        # """,
        """
        function void more() {  // Added to test Jack syntax that is not used in
            var int i, j;       // the Square files.
            var String s;
            var Array a;
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
            return;
        }
        """,
    ]
    sample_subroutine_dec_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_subroutine_dec]

    for ts in sample_subroutine_dec_tokenstreams:
        res = parser_tester(ts, "subroutine_dec")
        indent(res)
        dump(res)
        assert res
    print("finished")


