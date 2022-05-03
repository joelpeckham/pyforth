from pydoc import doc
from state import State
from typing import Dict
from word import primitiveWord

Primitives: Dict[str, primitiveWord] = {}


def forthPrimitive(func) -> None:
    ds = func.__doc__  # Docstring
    lexeme = ds[ds.find("Lexeme: ") + 8:].split()[0].strip()
    compiletime = ds[ds.find("Compiletime: ") + 8:].split()[0].strip() == "True"
    if lexeme not in Primitives:
        Primitives[lexeme] = primitiveWord(lexeme)
    if compiletime:
        Primitives[lexeme].compile = func
    else:
        Primitives[lexeme].run = func


@forthPrimitive
def prim_0(state: State):
    """
    Push the integer 0 onto the stack.
    Stack effect: - 0
    Lexeme: 0
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_0_less_than(state: State):
    """
    Return a true FLAG if N1 is negative.
    Stack effect: N1 - FLAG
    Lexeme: 0<
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_0_equality_sign(state: State):
    """
    Return a true FLAG if N1 is zero.
    Stack effect: N1 - FLAG
    Lexeme: 0=
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_0f(state: State):
    """
    Return a true FLAG if N1 is greater than zero.
    Stack effect: N1 - FLAG
    Lexeme: 0F
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_0branch(state: State):
    """
    If N1 is false (value is 0) perform a branch to the
    address in the next program cell, otherwise continue.
    Stack effect: N1 -
    Lexeme: 0BRANCH
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_1_plus(state: State):
    """
    Add one to N1, returning N2.
    Stack effect: N1 - N2
    Lexeme: 1+
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_1_minus(state: State):
    """
    Subtract one from N1, returning N2.
    Stack effect: N1 - N2
    Lexeme: 1-
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_2_plus(state: State):
    """
    Add two to N1, returning N2.
    Stack effect: N1 - N2
    Lexeme: 2+
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_2_asterisk(state: State):
    """
    Multiply N1 by two, returning N2.
    Stack effect: N1 - N2
    Lexeme: 2*
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_2_slash(state: State):
    """
    Divide N1 by two, returning N2.
    Stack effect: N1 - N2
    Lexeme: 2/
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_4_plus(state: State):
    """
    Add four to N1, returning N2.
    Stack effect: N1 - N2
    Lexeme: 4+
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_less_than(state: State):
    """
    Return a true FLAG if N1 is less than N2.
    Stack effect: N1 N2 - FLAG
    Lexeme: <
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_less_than_greater_than(state: State):
    """
    Return a true FLAG if N1 is not equal to N2.
    Stack effect: N1 N2 - FLAG
    Lexeme: <>
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_equality_sign(state: State):
    """
    Return a true FLAG if N1 equals N2.
    Stack effect: N1 N2 - FLAG
    Lexeme: =
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_r(state: State):
    """
    Push N1 onto the return stack.
    Stack effect: N1 -
    Lexeme: R
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_greater_than(state: State):
    """
    Return a true FLAG if N1 is greater than N2.
    Stack effect: N1 N2 - FLAG
    Lexeme: >
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_exclamation_mark(state: State):
    """
    Store N1 at location ADDR in program memory.
    Stack effect: N1 ADDR -
    Lexeme: !
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_plus(state: State):
    """
    Add N1 and N2, giving sum N3.
    Stack effect: N1 N2 - N3
    Lexeme: +
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_plus_exclamation_mark(state: State):
    """
    Add N1 to the value pointed to by ADDR.
    Stack effect: N1 ADDR -
    Lexeme: +!
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_minus(state: State):
    """
    Subtract N2 from N1, giving difference N3.
    Stack effect: N1 N2 - N3
    Lexeme: -
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_colon(state: State):
    """
    Define the start of a subroutine.  The primitive
    [CALL] is compiled every time this subroutine is
    reference by other definitions.
    Stack effect: -
    Lexeme: :
    Compiletime: False
    """
    state.compileFlag = True


@forthPrimitive
def prim_semicolon(state: State):
    """
    Perform a subroutine return and end the definition
    of a subroutine.  The primitive [EXIT] is compiled.
    Stack effect: -
    Lexeme: ;
    Compiletime: False
    """
    state.compileFlag = False
    returnAddress = state.returnStack.pop()
    state.programCounter = returnAddress


@forthPrimitive
def prim_question_markdup(state: State):
    """
               N1 - N1      ( if N1 is zero  )
    Conditionally duplicate the input N1 if it is
    non-zero.
    Stack effect: N1 - N1 N1 ( if N1 non-zero )
    Lexeme: ?DUP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_at_sign(state: State):
    """
    Fetch the value at location ADDR in program memory,
    returning N1.
    Stack effect: ADDR - N1<
    Lexeme: @
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_abs(state: State):
    """
    Take the absolute value of N1 and return the result N2.
    Stack effect: N1 - N2
    Lexeme: ABS
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_and(state: State):
    """
    Perform a bitwise AND on N1 and N2, giving result N3.
    Stack effect: N1 N2 - N3
    Lexeme: AND
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_branch(state: State):
    """
    Perform an unconditional branch to the compiled in-line
    address.
    Stack effect: -
    Lexeme: BRANCH
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_d_exclamation_mark(state: State):
    """
    Store the double-precision value D1 at the two memory
    words starting at ADDR.
    Stack effect: D1 ADDR -
    Lexeme: D!
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_d_plus(state: State):
    """
    Return the double precision sum of D1 and D2 as D3.
    Stack effect: D1 D2 - D3
    Lexeme: D+
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_d_at_sign(state: State):
    """
    Fetch the double precision value D1 from memory starting
    at address ADDR.
    Stack effect: ADDR - D1
    Lexeme: D@
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_ddrop(state: State):
    """
    Drop the double-precision integer D1.
    Stack effect: D1 -
    Lexeme: DDROP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_ddup(state: State):
    """
    Duplicate D1 on the stack.
    Stack effect: D1 - D1 D1
    Lexeme: DDUP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_dnegate(state: State):
    """
    Return D2, which is the two's complement of D1.
    Stack effect: D1 - D2
    Lexeme: DNEGATE
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_drop(state: State):
    """
    Drop N1 from the stack.
    Stack effect: N1 -
    Lexeme: DROP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_dswap(state: State):
    """
    Swap the top two double-precision numbers on the stack.
    Stack effect: D1 D2 - D2 D1
    Lexeme: DSWAP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_dup(state: State):
    """
    Duplicate N1, returning a second copy of it on the stack.
    Stack effect: N1 - N1 N1
    Lexeme: DUP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_i(state: State):
    """
    Return the index of the currently active loop.
    Stack effect: - N1
    Lexeme: I
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_i_single_quote(state: State):
    """
    Return the limit of the currently active loop.
    Stack effect: - N1
    Lexeme: I'
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_j(state: State):
    """
    Return the index of the outer loop in a nested loop structure.
    Stack effect: - N1
    Lexeme: J
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_leave(state: State):
    """
    Set the loop counter on the return stack equal to the
    loop limit to force an exit from the loop.
    Stack effect: -
    Lexeme: LEAVE
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_lit(state: State):
    """
    Treat the compiled in-line value as an integer constant,
    and push it onto the stack as N1.
    Stack effect: - N1
    Lexeme: LIT
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_negate(state: State):
    """
    Return N2, which is the two's complement of N1
    NOP           -
    Do nothing.
    Stack effect: N1 - N2
    Lexeme: NEGATE
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_not(state: State):
    """
    Synonym for 0=.  Takes the inverse of a flag value.
    Stack effect: FLAG1 - FLAG2
    Lexeme: NOT
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_or(state: State):
    """
    Perform a bitwise OR on N1 and N2, giving result N3.
    Stack effect: N1 N2 - N3
    Lexeme: OR
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_over(state: State):
    """
    Push a copy of the second element on the stack, N1, onto
    the top of the stack.
    Stack effect: N1 N2 - N1 N2 N1
    Lexeme: OVER
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_pick(state: State):
    """
    Copy the N1'th element deep in the data stack to the top.
    In Forth-83, 0 PICK is equivalent to DUP , and 1 PICK 
    is equivalent to OVER .
    Stack effect: ... N1 - ... N2
    Lexeme: PICK
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_r_greater_than(state: State):
    """
    Pop the top element of the return stack, and push it onto
    the data stack as N1.
    Stack effect: - N1
    Lexeme: R>
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_r_at_sign(state: State):
    """
    Copy the top Return Stack word N1 onto the Data Stack.
    Stack effect: - N1
    Lexeme: R@
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_roll(state: State):
    """
    Pull the N1'th element deep in the data stack to the top,
    closing the hole left in the stack.  In Forth-83, 1 ROLL
    is equivalent to SWAP , and 2 ROLL is equivalent to ROT.
    Stack effect: ... N1 - ... N2
    Lexeme: ROLL
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_rot(state: State):
    """
    Pull the third element down in the stack onto the top of
    the stack.
    Stack effect: N1 N2 N3 - N2 N3 N1
    Lexeme: ROT
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_s_minusd(state: State):
    """
    Sign extend N1 to occupy two words, making it a double
    precision integer D2.
    Stack effect: N1 - D2
    Lexeme: S-D
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_swap(state: State):
    """
    Swap the order of the top two stack elements.
    Stack effect: N1 N2 - N2 N1
    Lexeme: SWAP
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_u_less_than(state: State):
    """
    Return a true FLAG if U1 is less than U2 when compared
    as unsigned integers.
    Stack effect: U1 U2 - FLAG
    Lexeme: U<
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_u(state: State):
    """
    Return a true FLAG if U1 is greater than U2 when compared
    as unsigned integers.
    Stack effect: U1 U2 - FLAG
    Lexeme: U
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_u_asterisk(state: State):
    """
    Perform unsigned integer multiplication on N1 and N2,
    yielding the unsigned double precision result D3.
    Stack effect: N1 N2 - D3
    Lexeme: U*
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_u_slashmod(state: State):
    """
    Perform unsigned integer division on D1 and N2, yielding
    the quotient N4 and the remainder N3.
    Stack effect: D1 N2 - N3 N4
    Lexeme: U/MOD
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_xor(state: State):
    """
    Perform a bitwise exclusive OR on N1 and N2, giving result N3.
    Stack effect: N1 N2 - N3
    Lexeme: XOR
    Compiletime: False
    """
    pass


@forthPrimitive
def prim_execute(state: State):
    """
    Execute the code starting at ADDR.
    Stack effect: ADDR -
    Lexeme: EXECUTE
    Compiletime: False
    """
    address = state.dataStack.pop()
    state.programCounter = address
