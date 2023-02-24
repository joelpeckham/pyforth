# pyforth | FORTH in 130* lines of Python
## Introduction

FORTH is a simple stack-based language. It is a great language to learn about compilers and interpreters. This article will show you how to write a FORTH compiler and interpreter in 130* lines of Python.

### Some disclaimers

* Firstly, this is not a perfect, standards compliant FORTH. It's just a fun little project to learn about compilers and interpreters. 
* Secondly, this is more of a rough guide and less of a tutorial. I'm not going to go into a lot of detail about how things work. I'm just going to show you how to get things working. If you want to learn more about compilers and interpreters, I recommend [Crafting Interpreters](https://craftinginterpreters.com/).
* Finally, it's really it's around 480 lines total, but since most of that is defining primitives which could be done runtime, it's not really relevant. It's just nice to have some starting points to work from :)

## A language in two parts

Our FORTH implementation will have two main states, a compile state and an interpret state. In the compile state, we will be collecting words to be executed later. In the interpret state, we will be executing the words we have collected.

To get started let's make a file called `state.py`. This file will contain two dataclasses to represent the two states of our FORTH implementation.

First we need to import some things from the `dataclasses` module.
```python
from dataclasses import dataclass, field
```
Then we can define our two states.
If you are not familiar with dataclasses, they are a nice way to define classes that are just containers for data. They are a great way to define simple classes that don't need any methods. You can read more about them [in the Python docs](https://docs.python.org/3/library/dataclasses.html).

```python
@dataclass
class CompileState:
    tokens: list        = field(default_factory=list)
    codes: list         = field(default_factory=list)
    branchStack: list   = field(default_factory=list)
    variables: dict     = field(default_factory=dict)
    words: dict         = field(default_factory=dict)
    pos: int            = 0
    last_return: int    = 0
    end: bool           = False

@dataclass
class InterpretState:
    codes: list         = field(default_factory=list)
    dataStack: list     = field(default_factory=list)
    branchStack: list   = field(default_factory=list)
    variables: list     = field(default_factory=list)
    pos: int            = 0
    end: bool           = False
```

## We all need a little help

Next, we'll define some helper functions to make our lives easier. We'll put these in a file called `helpers.py`.

```python3
from typing import List

def tokenize(code:str) -> List[str]:
    tokensOut : List[str] = []
    tokensOut = code.split()
    return tokensOut

def isInt(lexeme:str) -> bool:
        try:
            int(lexeme)
        except ValueError:
            return False
        return True
```

These two small funtions will help us by splitting our code into small pieces called tokens and by checking if a given lexeme is an integer.

## Getting primitive

Next, we'll define some primitives. These are the basic building blocks of our language. We'll put these in a file called `primitives.py`.

Let's start by importing some things we'll need.
```python3
from __future__ import annotations
from typing import Dict, Callable
from state import InterpretState, CompileState
from getch import getch
```
Getch is a bit special. It's a library that allows us to get a single character from the user without having to press enter. It's not a standard library, so you'll have to install it with `pip install getch`.  

Next we'll define a dictionary to hold all of our primitives. We'll call it `Primitives`.
```python
Primitives : Dict[str, Dict[str,function]] = {} #The main export of this file.
```

Now, we'll define a couple decorators. These will allow us to define primitives in a more concise way. The first decorator is called `primitive()`. It will take a function, strip intended lexeme from docstring, and add it to the `Primitives` dictionary. The rest of the logic helps us to tag which lexemes are compile only and which are interpret only, and which are both. 

```python
def primitive(func) -> None:
    """
    Decorator which automatically adds a primitve word to the Primitives dictionary.
    It creates a default compile-time behavior for the primitive if none is provided.
    Lexemes for the primitives must be provided in the docstring of the function.
    """
    docstring = func.__doc__
    specialCompile : bool = docstring.find(" | (Function Implements Special Compile-Time Behavior)") != -1
    lexeme = docstring[docstring.find("Lexeme: ") + 8:].split()[0].strip()
    funcs = Primitives.get(lexeme, {"compile": None, "execute": None})
    if specialCompile:
        funcs["compile"] = func
    else:
        defaultCompile : Callable[[CompileState], None] = lambda state: state.codes.append(lexeme)
        funcs["compile"] = defaultCompile
        funcs["execute"] = func
    Primitives[lexeme] = funcs
```

The second decorator is called `compileTime()`. This will simply add a marker to the docstring of the function to indicate that it implements special compile-time behavior. This is useful for primitives that need to do something special when they are compiled, but also need to do something special when they are executed. 

```python
def compileTime(func) -> function:
    """
    Decorator to mark a primitive as having a non-default compile-time behavior.
    """
    func.__doc__ = func.__doc__ + " | (Function Implements Special Compile-Time Behavior)"
    return func
```

Lastly in this `primitives.py` file, we'll define some primitives. We'll start with some simple ones that don't need any special compile-time behavior. You can stop here, but I suggest you use all of them to see how they work.

```python
@primitive
def plus(state:InterpretState) -> None:
    """Lexeme: +"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(a + b)
    state.pos += 1

@primitive
def minus(state:InterpretState) -> None:
    """Lexeme: -"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b - a)
    state.pos += 1

@primitive
def star(state:InterpretState) -> None:
    """Lexeme: *"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(a * b)
    state.pos += 1

@primitive
def slash(state:InterpretState) -> None:
    """Lexeme: /"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b // a)
    state.pos += 1

@primitive
def mod(state:InterpretState) -> None:
    """Lexeme: MOD"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b % a)
    state.pos += 1

@primitive
def slashMod(state:InterpretState) -> None:
    """Lexeme: /MOD"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b % a)
    state.dataStack.append(b // a)
    state.pos += 1

@primitive
def lessThan(state:InterpretState) -> None:
    """Lexeme: <"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    if a < b:
        state.dataStack.append(-1)
    else:
        state.dataStack.append(0)
    state.pos += 1

@primitive
def greaterThan(state:InterpretState) -> None:
    """Lexeme: >"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    if a > b:
        state.dataStack.append(-1)
    else:
        state.dataStack.append(0)
    state.pos += 1

@primitive
def equal(state:InterpretState) -> None:
    """Lexeme: ="""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    if a == b:
        state.dataStack.append(-1)
    else:
        state.dataStack.append(0)
    state.pos += 1

@primitive
def bitwiseAnd(state:InterpretState) -> None:
    """Lexeme: AND"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(a & b)
    state.pos += 1

@primitive
def bitwiseOr(state:InterpretState) -> None:
    """Lexeme: OR"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(a | b)
    state.pos += 1

@primitive
def bitwiseNot(state:InterpretState) -> None:
    """Lexeme: INVERT"""
    a = state.dataStack.pop()
    state.dataStack.append(~a)
    state.pos += 1

@primitive
def swap(state:InterpretState) -> None:
    """Lexeme: SWAP"""
    a, b = state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(a)
    state.dataStack.append(b)
    state.pos += 1

@primitive
def dup(state:InterpretState) -> None:
    """Lexeme: DUP"""
    a = state.dataStack.pop()
    state.dataStack.append(a)
    state.dataStack.append(a)
    state.pos += 1

@primitive
def drop(state:InterpretState) -> None:
    """Lexeme: DROP"""
    state.dataStack.pop()
    state.pos += 1

@primitive
def over(state:InterpretState) -> None:
    """Lexeme: OVER"""
    state.dataStack.append(state.dataStack[-2])
    state.pos += 1

@primitive
def rot(state:InterpretState) -> None:
    """Lexeme: ROT
    ( n1 n2 n3 -- n2 n3 n1 )
    """
    a, b, c = state.dataStack.pop(), state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b)
    state.dataStack.append(a)
    state.dataStack.append(c)
    state.pos += 1

@primitive
def twoSwap(state:InterpretState) -> None:
    """
    Lexeme: 2SWAP
    ( x1 x2 x3 x4 -- x3 x4 x1 x2 )
    """
    a, b, c, d = state.dataStack.pop(), state.dataStack.pop(), state.dataStack.pop(), state.dataStack.pop()
    state.dataStack.append(b)
    state.dataStack.append(a)
    state.dataStack.append(d)
    state.dataStack.append(c)
    state.pos += 1

@primitive
def twoOver(state:InterpretState) -> None:
    """
    Lexeme: 2OVER
    ( x1 x2 x3 x4 -- x1 x2 x3 x4 x1 x2 )
    """
    state.dataStack.append(state.dataStack[-4])
    state.dataStack.append(state.dataStack[-4])
    state.pos += 1

@primitive
def twoDrop(state:InterpretState) -> None:
    """
    Lexeme: 2DROP
    ( x1 x2 x3 x4 -- x1 x2 )
    """
    state.dataStack.pop()
    state.dataStack.pop()
    state.pos += 1

@primitive
def key(state:InterpretState) -> None:
    """Lexeme: KEY"""
    keypress = getch()
    state.dataStack.append(ord(keypress))
    state.pos += 1

@primitive
def DEBUG(state:InterpretState) -> None:
    """Lexeme: DEBUG"""
    print(state.dataStack)
    state.pos += 1

@primitive
def period(state:InterpretState) -> None:
    """Lexeme: ."""
    print(state.dataStack.pop(), end='\n')
    state.pos += 1

@primitive
def emit(state:InterpretState) -> None:
    """Lexeme: EMIT"""
    print(chr(state.dataStack.pop()))
    state.pos += 1

@primitive
def cr(state:InterpretState) -> None:
    """Lexeme: CR"""
    print()
    state.pos += 1

@primitive
def semicolon(state:InterpretState) -> None:
    """Lexeme: ;"""
    state.pos = state.branchStack.pop()

@primitive 
@compileTime
def semicolon(state:CompileState) -> None:
    """Lexeme: ;"""
    state.codes.append(";")
    state.last_return = len(state.codes)

@primitive
@compileTime
def colon(state:CompileState) -> None:
    """Lexeme: :"""
    word = state.tokens[state.pos+1]
    state.words[word] = len(state.codes)
    state.pos += 1

@primitive
def push(state:InterpretState) -> None:
    """Lexeme: PUSH"""
    value = state.codes[state.pos+1]
    state.dataStack.append(value)
    state.pos += 2

@primitive
@compileTime
def push(state:CompileState) -> None:
    """Lexeme: PUSH has no compile-time behavior"""
    return None

@primitive
def call(state:InterpretState) -> None:
    """Lexeme: CALL"""
    state.branchStack.append(state.pos + 2)
    state.pos = state.codes[state.pos+1]

@primitive
@compileTime
def call(state:CompileState) -> None:
    """Lexeme: CALL has no compile-time behavior"""
    return None

@primitive
def end(state:InterpretState) -> None:
    """Lexeme: END"""
    state.end = True

@primitive
@compileTime
def end(state:CompileState) -> None:
    """Lexeme: END has no compile-time behavior"""
    return None

@primitive
def prim_if(state:InterpretState) -> None:
    """Lexeme: IF"""
    if state.dataStack.pop() == 0:
        state.pos = state.codes[state.pos+1]
    else:
        state.pos += 2

@primitive
@compileTime
def prim_if(state:CompileState) -> None:
    """Lexeme: IF"""
    state.branchStack.append(len(state.codes) + 1)
    state.codes.extend(("IF", None))

@primitive
def prim_else(state:InterpretState) -> None:
    """Lexeme: ELSE"""
    state.pos = state.codes[state.pos+1]

@primitive
@compileTime
def prim_else(state:CompileState) -> None:
    """Lexeme: ELSE"""
    ifPos = state.branchStack.pop()
    state.codes[ifPos] = len(state.codes) + 2
    state.branchStack.append(len(state.codes) + 1)
    state.codes.extend(("ELSE", None))

@primitive
@compileTime
def prim_then(state:CompileState) -> None:
    """Lexeme: THEN"""
    elsePos = state.branchStack.pop()
    state.codes[elsePos] = len(state.codes)

@primitive
def do(state:InterpretState) -> None:
    """Lexeme: DO"""
    a,b = state.dataStack.pop(), state.dataStack.pop()
    state.branchStack.extend((b,a))
    state.pos += 1

@primitive
@compileTime
def do(state:CompileState) -> None:
    """Lexeme: DO"""
    state.branchStack.append(len(state.codes) + 1)
    state.codes.append("DO")

@primitive
def loop(state:InterpretState) -> None:
    """Lexeme: LOOP"""
    a,b = state.branchStack.pop(), state.branchStack.pop()
    a += 1
    if a < b:
        state.branchStack.extend((b,a))
        state.pos = state.codes[state.pos+1]
    else:
        state.pos += 2

@primitive
@compileTime
def loop(state:CompileState) -> None:
    """Lexeme: LOOP"""
    doPos = state.branchStack.pop()
    state.codes.extend(("LOOP", doPos))

@primitive
@compileTime
def variable(state:CompileState) -> None:
    """Lexeme: VARIABLE"""
    varName = state.tokens[state.pos+1]
    state.variables[varName] = len(state.variables)
    state.pos += 1

@primitive
def at(state:InterpretState) -> None:
    """Lexeme: @"""
    a,b = state.dataStack.pop(), state.dataStack.pop()
    state.variables[a] = b
    state.pos += 1

@primitive
def bang(state:InterpretState) -> None:
    """Lexeme: !"""
    a = state.dataStack.pop()
    state.dataStack.append(state.variables[a])
    state.pos += 1

@primitive
def I(state:InterpretState) -> None:
    """Lexeme: I"""
    state.dataStack.append(state.branchStack[-1])
    state.pos += 1
```

## Interpreter

The interpreter itself is very small. It's just a loop that runs until the end of the program is reached. Then, token by token, it looks each token in the dictionary of primitives and calls the function associated with it. If the token is not in the dictionary, it is assumed to be a number and is pushed onto the data stack.

There's more going on here to deal with variables and calling "functions", but again, this isn't a tutorial.

```python
from state import InterpretState, CompileState
from primitives import Primitives
from helpers import isInt

class Interpreter:
    def __init__(self):
        self.compileState = CompileState()
        self.interpretState = InterpretState()
    
    def run(self, tokens): self.compile(self.compileState, tokens)

    def compile(self, state:CompileState, tokens):
        state.tokens.extend(tokens)
        if state.codes:
            state.codes.pop()
        state.end = False

        while not state.end:
            if state.pos == len(state.tokens):
                state.codes.append('END')
                state.end = True
                break

            token = state.tokens[state.pos]
            if isInt(token):
                state.codes.extend(('PUSH', int(token)))
            elif token in Primitives:
                Primitives[token]['compile'](state)
            elif token in state.variables:
                state.codes.extend(('PUSH', state.variables[token]))
            elif token in state.words:
                state.codes.extend(('CALL', state.words[token]))
            else:
                print('Unknown word:', token)
            state.pos += 1
        self.interpret(self.interpretState, state.codes, len(state.variables), state.last_return)

    def interpret(self, state: InterpretState, codes, var_count, start):
        state.codes = codes
        state.variables.extend([0] * (var_count - len(state.variables)))
        state.pos = max(start, state.pos)
        state.end = False

        while not state.end:
            code = state.codes[state.pos]
            Primitives[code]['execute'](state)
```
## Making it interactive

The interpreter is now ready to be used. I've added a simple REPL to make it easier to use. It's not very sophisticated, but it's short and it works.

Let's add this code to a file called `pyforth.py`:

```python
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
```

### Woo! It's done!

Make sure you've added the correct python install path to the shebang at the top, then run with `./pyforth.py` and you should be good to go!


[Video Presentation](https://youtu.be/Yu81m0RjT6w)
