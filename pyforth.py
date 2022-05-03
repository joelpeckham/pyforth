#! /usr/local/bin/python3
import helpers, interpreter, argparse, readline # Readline magically makes input history work. 🙃🔫

# Get command line arguments.
parser = argparse.ArgumentParser(description='Forth Interpreter')
parser.add_argument('file', nargs='?', type=argparse.FileType('r'))
args = parser.parse_args()

# Decide if we're reading from a file or stdin.
if not bool(args.file):
    forth = interpreter.Interpreter()
    while True:
        try: line = input('> ')
        except (EOFError, KeyboardInterrupt): break
        forth.run(helpers.tokenize(line))
else:
    forth = interpreter.Interpreter()
    forth.run(helpers.tokenize(args.file.read()))