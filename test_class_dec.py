from typing import List, Iterable, cast
from xml.etree.ElementTree import dump, Element

from utils import make_tokenstream, parser_tester, indent

if __name__ == "__main__":
    sample_class_dec: list[str] = [
        # """
        # class Main {
        #     static boolean test;    // Added for testing -- there is no static keyword
        #                             // in the Square files.
        #     function void main() {
        #         var SquareGame game;
        #         let game = SquareGame.new();
        #         do game.run();
        #         do game.dispose();
        #         return;
        #     }

        #     function void more() {  // Added to test Jack syntax that is not used in
        #         var int i, j;       // the Square files.
        #         var String s;
        #         var Array a;
        #         if (false) {
        #             let s = "string constant";
        #             let s = null;
        #             let a[1] = a[2];
        #         }
        #         else {              // There is no else keyword in the Square files.
        #             let i = i * (-j);
        #             let j = j / (-2);   // note: unary negate constant 2
        #             let i = i | j;
        #         }
        #         return;
        #     }
        # }
        # """,
        # """
        # class Main {
        #     function void main() {
        #         var Array a;
        #         var int length;
        #         var int i, sum;
            
        #         let length = Keyboard.readInt("HOW MANY NUMBERS? ");
        #         let a = Array.new(length);
        #         let i = 0;
                
        #         while (i < length) {
        #             let a[i] = Keyboard.readInt("ENTER THE NEXT NUMBER: ");
        #             let i = i + 1;
        #         }
                
        #         let i = 0;
        #         let sum = 0;
                
        #         while (i < length) {
        #             let sum = sum + a[i];
        #             let i = i + 1;
        #         }
                
        #         do Output.printString("THE AVERAGE IS: ");
        #         do Output.printInt(sum / length);
        #         do Output.println();
                
        #         return;
        #     }
        # }
        # """,
        """
        class Square {

        field int x, y; 
        field int size; 

        constructor Square new(int Ax, int Ay, int Asize) {
            let x = Ax;
            let y = Ay;
            let size = Asize;
            do draw();
            return x;
        }

        method void dispose() {
            do Memory.deAlloc(this);
            return;
        }

        method void draw() {
            do Screen.setColor(x);
            do Screen.drawRectangle(x, y, x, y);
            return;
        }

        method void erase() {
            do Screen.setColor(x);
            do Screen.drawRectangle(x, y, x, y);
            return;
        }

        method void incSize() {
            if (x) {
                do erase();
                let size = size;
                do draw();
            }
            return;
        }

        method void decSize() {
            if (size) {
                do erase();
                let size = size;
                do draw();
            }
            return;
        }

        method void moveUp() {
            if (y) {
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
                let y = y;
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
            }
            return;
        }

        method void moveDown() {
            if (y) {
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
                let y = y;
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
            }
            return;
        }

        method void moveLeft() {
            if (x) {
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
                let x = x;
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
            }
            return;
        }

        method void moveRight() {
            if (x) {
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
                let x = x;
                do Screen.setColor(x);
                do Screen.drawRectangle(x, y, x, y);
            }
            return;
        }
        }  
        """

    ]
    sample_class_dec_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_class_dec]

    for ts in sample_class_dec_tokenstreams:
        working_on: str = ''.join([cast(str, x.text) for x in cast(Iterable[Element], ts)])
        print(f"working on: {working_on}")
        res = parser_tester(ts, "klass", debug=True)
        indent(res)
        dump(res)
        assert res

    # e: ElementTree = ElementTree(res)
    # e.write("testclass.xml")

    print("finished")

