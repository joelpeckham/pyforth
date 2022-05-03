from __future__ import annotations
from typing import Dict, Callable
from state import InterpretState, CompileState
from getch import getch

Primitives : Dict[str, Dict[str,function]] = {} #The main export of this file.

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
    
def compileTime(func) -> function:
    """
    Decorator to mark a primitive as having a non-default compile-time behavior.
    """
    func.__doc__ = func.__doc__ + " | (Function Implements Special Compile-Time Behavior)"
    return func

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