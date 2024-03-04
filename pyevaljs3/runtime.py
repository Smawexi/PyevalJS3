"""
feature: Added filtering warnings from version 0.1
"""

__package__ = "pyevaljs3"

import os
import subprocess
import logging
import json
import abc
import tempfile

from . import exception
JSException = exception.JSException
_logger = logging.getLogger("JSEval")


def get_node_env():
    node = os.environ.get('NODE_PATH') if os.environ.get('NODE_PATH') else os.environ.get('NODE')
    if not node:
        return "node"
    return node


class AbstractRuntime:

    @abc.abstractmethod
    def eval(self, code: str = None):
        raise NotImplementedError()

    @abc.abstractmethod
    def compile(self, source: str = None, suffix: str = None):
        raise NotImplementedError()

    def _eval(self, code: str = None, ignore_output=False):
        node = get_node_env()
        _cmd = [node, "--no-warnings"]
        _input = f'var __result = (() => {{{code}}})();if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}};'
        popen = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 universal_newlines=True, creationflags=subprocess.DETACHED_PROCESS)
        try:
            outs, errs = popen.communicate(input=_input)
        except Exception as e:
            _logger.error(e)
            popen.kill()
            outs, errs = popen.communicate()

        if popen.returncode != 0:
            raise JSException(outs)

        return self._extract_result(outs, ignore_output)

    @staticmethod
    def _extract_result(outs: str, ignore_output=False):
        if not outs.strip().split("\n")[0]:
            return
        try:
            for out in outs.strip().split("\n")[:-2]:
                if not ignore_output:
                    print(out)
            if outs.strip().split("\n")[-2] == "JSEval_state: ok":
                try:
                    return json.loads(outs.strip().split()[-1])
                except json.JSONDecodeError:
                    _logger.error("not supported this behaviour")
                    return None
            else:
                if not ignore_output:
                    print(outs.strip().split()[-2])
                    print(outs.strip().split()[-1])
        except IndexError:
            if not ignore_output:
                print(outs.strip().split("\n")[-1])


class AbstractContext:

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        raise NotImplementedError()

    def _call(self, func, args):
        node = get_node_env()
        _source = f'{self._source};var __result = {func}.apply(this, {args});if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}}'
        _path = self._make_temp_file(_source)
        _cmd = [node, "--no-warnings", _path]
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
