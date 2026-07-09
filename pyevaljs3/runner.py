__package__ = "pyevaljs3"

import json
from typing import List
from ._node_program import NODE_CALL, NODE_EVAL, NODE_ASYNC_CALL


NODE_PROGRAM = {
    'call': NODE_CALL,
    'eval': NODE_EVAL,
    'async_call': NODE_ASYNC_CALL
}


class Runner:

    @classmethod
    def program(cls, action: str, code: str, func=None, args: List = None):
        if action == 'call' or action == "async_call":
            _args = json.dumps(args, ensure_ascii=False)
            return NODE_PROGRAM[action].format(_source=code, func=func, args=_args)

        return NODE_PROGRAM[action].format(code=code)
