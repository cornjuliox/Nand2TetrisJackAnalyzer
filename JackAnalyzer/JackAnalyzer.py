import sys
import os
from typing import List
from pathlib import Path

from Tokenizer import TokenBuilder, RULES
from Writer import token_fucker, xml_fucker

if __name__ == "__main__":
    try:
        infile: str = sys.argv[1]
    except IndexError:
        print("usage: JackAnalyzer.py <inputFileOrDirectory>")
        sys.exit()

    inpath: Path = Path(infile)
    for_processing: List[str] = []
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
            raw_contents: List[str] = F.read()

        contents: str = raw_contents

        tb: TokenBuilder = TokenBuilder(contents, RULES)
        print(f"-> Tokenizing {filepath}.")
        tokens: List[tuple] = [x for x in tb if x and x.type not in ["COMMENT", "STAR_COMMENT"]]
        print(f"-> Converting {filepath} tokens to tags.")
        tags: List[str] = [token_fucker(x) for x in tokens]
        print("-> Generating final XML.")
        xml: str = xml_fucker(tags)
        result: tuple = (filepath, xml)
        results.append(result)

    for x in results:
        print("-> Writing output files.")
        
        # NOTE: I need to change the name of the file
        #       both name AND extension
        #       simply changing the suffix will overwrite
        #       the test files in the project directory.
        oldfile: Path = x[0]
        original_name: str = oldfile.stem
        new_name: str = f"enricojr-{original_name}"
        new_path: Path = oldfile.with_stem(new_name)
        new_file: Path = new_path.with_suffix(".xml")
        print(f"-> Renamed {oldfile} to {new_file}")

        with new_file.open("w") as F:
            F.write(x[1])

        print(f"-> File {new_file} successfully written.")
    
    print("-> Program complete!")


