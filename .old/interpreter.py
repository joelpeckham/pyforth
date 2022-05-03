from state import State
from helpers import isInt, Token
from typing import List
from primitives import Primitives
from word import primitiveWord

class Interpreter:
    def __init__(self, code:List[Token]) -> None:
        self.state = State()
        self.state.code = code
        self.state.dictionary.update(Primitives.primitives)

    def interpret(self, startingPoint = 0) -> None:
        """
        Interpret the code.
        """
        self.state.programCounter = startingPoint

        while self.state.programCounter < len(self.state.code):
            tokenObject = self.state.code[self.state.programCounter]
            token = tokenObject.lexeme
            if isInt(token):
                self.state.dataStack.append(token)
            elif token in self.state.dictionary:
                word = self.state.dictionary[token]
                if type(word) == primitiveWord:
                    if self.state.compileFlag:
                        word.compile(self.state)
                    else:
                        word.run(self.state)
                elif type(word) == int:
                    self.state.returnStack.append(self.state.programCounter)
                    self.state.dataStack.append(word)
                    self.state.dictionary["EXECUTE"].run(self.state)

                    
            else:
                print(f"Unknown token: {token}")