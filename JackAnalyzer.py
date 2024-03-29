import sys
import os
from typing import List
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree

from Tokenizer import TokenBuilder, RULES
from Token import KEYWORD_LIST
from Parser import JackParser
from utils import indent

if __name__ == "__main__":
    dispatch: dict = {
        "tokenize": None,
        "parse": None
    }
    try:
        infile: str = sys.argv[1]
    except IndexError:
        print("usage: JackAnalyzer.py <inputFileOrDirectory>")
        sys.exit()

    inpath: Path = Path(infile)
    for_processing: List[Path] = []
    print(f"-> currently working from {os.getcwd()}")
    if inpath.is_dir():
        print("-> <input> is directory")
        for jackfile in inpath.glob("*.jack"):
            for_processing.append(jackfile)
    else:
        print("-> <input> is a file")
        for_processing.append(inpath)

    print("-> JackAnalyzer v1")
    print(f"-> Analyzing the following files: {for_processing}")

    results: List[tuple] = []
    for filepath in for_processing:
        with filepath.open() as F:
            raw_contents: str = F.read()
        tb: TokenBuilder = TokenBuilder(raw_contents, RULES, KEYWORD_LIST)
        print(f"-> Tokenizing {filepath}.")

        raw_tokens: List[Element] = [x for x in tb if x is not None]
        # NOTE: I keep this in for debugging.
        # pretty_tokens: List[str] = [y.text for y in raw_tokens]
        # print(pretty_tokens)
        parser: JackParser = JackParser(tokens=raw_tokens)

        # NOTE: need to prep the token tree for the <file>T.xml file
        token_tree: Element = Element("tokens")
        token_tree.extend(raw_tokens)
        output_token_tree: ElementTree = ElementTree(token_tree)

        # NOTE: and this one is for the main <file>.xml
        class_tree: Element = parser.klass()
        output_parse_tree: ElementTree = ElementTree(class_tree)

        # NOTE: and now we use the built-in write, not the path write
        output_token_file_name: str = f"{filepath.stem}T.xml"
        # NOTE: If you don't use indent() it won't print properly,
        #       everything will end up being on one line.
        new_path_tokenized: Path = filepath.with_name(output_token_file_name)
        indent(output_token_tree)
        print("-> Writing tokenized file.")
        with new_path_tokenized.open("wb") as F:
            output_token_tree.write(F, short_empty_elements=False)

        output_class_file_name: str = f"{filepath.stem}.xml"
        new_path_parse_tree: Path = filepath.with_name(output_class_file_name)
        indent(output_parse_tree)
        print("-> Writing parse tree.")
        with new_path_parse_tree.open("wb") as F:
            output_parse_tree.write(F, short_empty_elements=False)
    
    print("-> Program complete!")


