from __future__ import annotations
from helpers import Position, Token, tokenize
from typing import List
from interpreter import Interpreter
import argparse

# Get command line arguments.
parser = argparse.ArgumentParser(description='Forth Interpreter')
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'))
args = parser.parse_args()

# Decide if we're reading from a file or stdin.
interactive_mode = not bool(args.file)

# Take our source code and pass it through each step of the compiler.
def runSourceCode(code:str) -> None:
    tokens : List[Token] = tokenize(code)
    interpreter = Interpreter(tokens)
    interpreter.interpret()

# Get the code and run it.
if interactive_mode:
    import readline # This magically makes input history work. 🙃🔫
    while True:
        try:
            line = input('> ')
        except (EOFError, KeyboardInterrupt):
            break
        runSourceCode(line)
else:
    fileText = args.file.read()
    runSourceCode(fileText)