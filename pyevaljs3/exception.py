class JSException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class RunTimeNotFoundError(Exception):
    """Missing node environment"""
