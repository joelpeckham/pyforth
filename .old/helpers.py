from collections import namedtuple
from dataclasses import dataclass
from typing import List

Position = namedtuple('Position', 'line column')

@dataclass
class Token:
    lexeme: str
    position: Position

    def __str__(self) -> str:
        return f"[Lexeme: '{self.lexeme}' Position: ({self.position.line}, {self.position.column})]"
    def __repr__(self) -> str: return self.__str__()

def tokenize(code:str) -> List[Token]:
    """
    Tokenizes a string of code. 
    Returns a list of Tuples, with a string with the token, 
    and a Position object with the line and column of the token in the source code.

    >>> tokenize("1 tree\\ndog 4")
    [[Lexeme: '1' Position: (1, 1)], [Lexeme: 'tree' Position: (1, 3)], [Lexeme: 'dog' Position: (2, 1)], [Lexeme: '4' Position: (2, 5)]]
    """

    tokensOut : List[Token] = []

    for lineNum, line in enumerate(code.splitlines()):
        tokens = line.split()
        columnPosition = 0
        for token in tokens:
            tokensOut.append(Token(token, Position(lineNum + 1, columnPosition + 1)))
            columnPosition += len(token) + 1
    return tokensOut

def isInt(lexeme:str) -> bool:
        try:
            int(lexeme)
        except ValueError:
            return False
        return True

if __name__ == "__main__":
    import doctest
    doctest.testmod()