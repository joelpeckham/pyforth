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