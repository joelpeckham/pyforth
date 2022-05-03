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