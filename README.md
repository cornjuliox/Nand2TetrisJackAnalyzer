# ABOUT
This is my WIP repository for the Nand2Tetris part 2 course on Coursera. The JackAnalyzer takes source code and creates an XML file containing an AST for any given Jack source file.

As of Jan 2023 it is incomplete, and the XML file only contains terminal symbols - keywords, symbols, and identifiers.
# What is this project?
This is my solution to Nand2Tetris' Project #10.

The goal is to tokenize + parse a series of files written in the Jack programming language, producing a pair of .xml files for each .jack file. One file will contain tokens representing the smallest elements of the Jack programming language, and the second will contain a tree representing a single Jack `class`.

# Usage
TODO

# Stack
- Python 3.10.4

# Known issues
- You might have noticed that the project isn't neatly organized into modules. This is because Coursera's grader will whine if there are any folders in the final submission so I've had to 'flatten' the typical project structure.
