import json
import os
import subprocess
import tempfile
import logging

__package__ = "pyevaljs3"
from . import runtime
from . import exception
JSException = exception.JSException
_logger = logging.getLogger("JSEval")
__all__ = ['JSEval', 'Context']


class JSEval(runtime.AbstractRuntime):

    def __init__(self):
        self._source = ''

    def compile(self, source: str = None, suffix: str = None) -> "Context":
        """
        编译javascript源代码
        :param source: 源代码字符串或要读取的文件路径
        :param suffix: js脚本文件名后缀(指定以什么模式执行), 默认是".js", 可选的值还有".cjs", ".mjs"等
        :return: Context
        """
        if os.path.isfile(source):
           source = open(source, encoding="utf-8").read()

        if source is not None:
            self._source += source
        else:
            raise ValueError("js source code is empty")

        if not suffix:
            suffix = ".js"
        if not suffix.__contains__("."):
            suffix = "." + suffix

        return Context(self._source, suffix)

    def eval(self, code: str = None):
        """
        执行javascript代码, 返回其结果(对于长字符串的情况，请使用compile)
        :param code:
        :return:
        """
        if code is None:
            return
        return self._eval(code)


class Context:

    def __init__(self, source: str = None, suffix: str = None):
        self._source = source
        self._suffix = suffix

    def call(self, func, *args):
        """
        调用指定的函数, 返回其结果
        :param func: 函数名
        :param args: 函数的参数列表
        :return:
        """
        if len(args) == 1:
            args = args[0]

        return self._call(func, list(args))

    def _call(self, func, args):
        _source = f'{self._source};var __result = {func}.apply(this, {args});if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}}'
        _path = self._make_temp_file(_source)
        _cmd = ['node', _path]
        popen = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 universal_newlines=True, creationflags=subprocess.DETACHED_PROCESS)
        try:
            outs, errs = popen.communicate()
        except Exception as e:
            _logger.error(e)
            popen.kill()
            outs, errs = popen.communicate()
        finally:
            os.remove(_path)

        if popen.returncode != 0:
            raise JSException(outs)

        return self._extract_result(outs)

    @staticmethod
    def _extract_result(outs: str):
        if not outs.strip().split("\n")[0]:
            return
        try:
            if outs.strip().split("\n")[-2] == "JSEval_state: ok":
                try:
                    return json.loads(outs.strip().split()[-1])
                except json.JSONDecodeError:
                    _logger.error("not supported this behaviour")
                    return None
        except IndexError:
            return

    def _make_temp_file(self, source: str = None):
        fd, path = tempfile.mkstemp(suffix=self._suffix, dir=".")
        with open(fd, 'w', encoding='utf-8') as fp:
            fp.write(source)
        return path
