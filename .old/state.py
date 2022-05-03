from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from helpers import Token
from myQueue import MyQueue

@dataclass
class State:
    """Global state of Forth interpreter."""
    dataStack: MyQueue = field(default_factory=MyQueue)
    returnStack: MyQueue = field(default_factory=MyQueue)
    dictionary: dict = field(default_factory=dict)
    compileFlag: bool = field(default=False)
    code: List[Token] = field(default_factory=list)
    programCounter: int = 0

