from typing import List
from xml.etree.ElementTree import indent, Element

from utils import make_tokenstream, parser_tester, dump

if __name__ == "__main__":
    sample_individual_body_var_dec: list[str] = [
        "var int i, j;",
        "var String s;",
        "var Array a;"

    ]
    sample_individual_body_var_dec_tokenstreams: List[List[Element]] = [make_tokenstream(x) for x in sample_individual_body_var_dec]

    for ts in sample_individual_body_var_dec_tokenstreams:
        # NOTE: Each line should be its own <vardec></vardec>
        res = parser_tester(ts, "subroutine_body_var_dec")
        indent(res)
        dump(res)
        assert res
    print("finished")
