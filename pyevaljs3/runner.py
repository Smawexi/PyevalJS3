__package__ = "pyevaljs3"

from typing import List
from ._node_program import NODE_CALL, NODE_EVAL


NODE_PROGRAM = {
    'call': NODE_CALL,
    'eval': NODE_EVAL
}


class Runner:

    @classmethod
    def program(cls, action: str, code: str, func=None, args: List = None):
        if action == 'call':
            return NODE_PROGRAM[action].format(_source=code, func=func, args=args)

        return NODE_PROGRAM[action].format(code=code)
