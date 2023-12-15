from __future__ import annotations

__package__ = 'pyevaljs3'
from . import evaljs as _evaljs


class JSEval:

    def compile(self, source: str = None, suffix: str = None) -> "Context":
        """
        编译javascript源代码
        :param source: 源代码字符串或要读取的文件路径
        :param suffix: js脚本文件名后缀(指定以什么模式执行), 默认是".js", 可选的值还有".cjs", ".mjs"等
        :return: Context
        """

    def eval(self, code: str = None):
        """
        执行javascript代码, 返回其结果(对于长字符串的情况，请使用compile)
        :param code:
        :return:
        """


class Context:

    def call(self, func, *args):
        """
        调用指定的函数, 返回其结果
        :param func: 函数名
        :param args: 函数的参数列表
        :return:
        """


def compile_(source: str = None, mode: str = None) -> Context:
    """
    编译js源代码
    :param source: 源代码字符串或要读取的文件路径
    :param mode: 执行模式, 默认以.js的行为去执行
    :return: Context
    """
    if mode is None:
        mode = ".js"

    return JSEval().compile(source, mode)


def eval_(code: str = None):
    """
    执行javascript代码, 返回其结果(对于长字符串的情况，请使用compile)
    :param code: js代码
    :return:
    """
    return JSEval().eval(code)


for obj_name in _evaljs.__all__:
    globals()[obj_name] = _evaljs.__dict__[obj_name]
