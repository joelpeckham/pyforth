from collections import deque
# Extention of collections.deque to prettify printing.
class MyQueue(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __str__(self) -> str:
        return f'[{", ".join(map(str, self))}]'