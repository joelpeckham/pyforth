from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from helpers import Position

class primitiveWord:
    def __init__(
        self, lexeme:str, 
        runtimeBehavior:function = None,
        compiletimeBehavior:function = None,
        position:Position = None) -> None:
        self.lexeme = lexeme
        self.run = runtimeBehavior
        self.compile = compiletimeBehavior
        self.sourcePos = position
    
    def __str__(self) -> str:
        return f"{self.lexeme} {self.sourcePos}"
    