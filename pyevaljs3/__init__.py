"""
简单示例
>>> import pyevaljs3
>>>
>>> js_code = "function f() {return 'ok';}; return f()"
>>> result = pyevaljs3.eval_(js_code)
>>> assert result == 'ok'
>>> # -------------------------------------------------------------------------------
>>> js_code = "function f(arg1, arg2) {console.log(arg1, arg2); return arg1 + arg2;}"
>>> ctx = pyevaljs3.compile_(js_code)
>>> result = ctx.call('f', 'a', 'b')
>>> assert result == 'ab'
>>> # 另外一种传参方式
>>> result = ctx.call('f', arg_list=['a', 'b'])
>>> assert result == 'ab'

# 还可以通过设置坏境变量来使用自定义版本的node, 只需设置NODE_PATH、NODE坏境变量即可, 如没设置则默认使用全局的node坏境(需要添加系统路径)
import os
# 优先级最高
os.environ['NODE_PATH'] = '/path/to/node.exe'
# 或者
os.environ['NODE'] = '/path/to/node.exe'
"""
from __future__ import annotations

__package__ = 'pyevaljs3'
from typing import List
from . import evaljs as _evaljs
from .__version__ import version


class JSEval:

    def compile(self, source: str = None, suffix: str = None) -> "Context":
        """
        编译javascript源代码
        :param source: 源代码字符串或要读取的文件路径
        :param suffix: js脚本文件名后缀(指定以什么模式执行), 默认是".js", 可选的值还有".cjs", ".mjs"等
        :return: Context
        """

    def eval(self, code: str = None, ignore_output=False):
        """
        执行javascript代码, 返回其结果
        :param code:
        :param ignore_output:
        :return: Any
        """


class Context:

    def call(self, func, *args, arg_list: List = None):
        """
        调用指定的函数, 返回其结果(若指定了arg_list, 优先使用它作为函数参数)
        :param func: 函数名
        :param args: 函数的参数列表
        :param arg_list: 函数的参数列表
        :return: Any
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


def eval_(code: str = None, ignore_output=False):
    """
    执行javascript代码, 返回其结果
    :param code: js代码
    :param ignore_output: 是否忽略执行过程中的输出, 若为True则仅返回其结果, 默认不忽略(False)
    :return: Any
    """
    return JSEval().eval(code, ignore_output)


for obj_name in _evaljs.__all__:
    globals()[obj_name] = _evaljs.__dict__[obj_name]
