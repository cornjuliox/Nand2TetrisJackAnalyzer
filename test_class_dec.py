from typing import List
from xml.etree.ElementTree import indent, dump

from JackAnalyzer.Token import Token, Node
from utils import make_tokenstream, parser_tester

if __name__ == "__main__":
    sample_class_dec: list[str] = [
        """
        class Main {
            static boolean test;    // Added for testing -- there is no static keyword
                                    // in the Square files.
            function void main() {
                var SquareGame game;
                let game = SquareGame.new();
                do game.run();
                do game.dispose();
                return;
            }

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
        }
        """
    ]
    sample_class_dec_tokenstreams: List[List[Token]] = [make_tokenstream(x) for x in sample_class_dec]

    for ts in sample_class_dec_tokenstreams:
        res = parser_tester(ts, "klass")
        indent(res)
        dump(res)
        assert res
    print("finished")

