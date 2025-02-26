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
import asyncio

from . import exception
from .setting import IS_WINDOWS, NO_WARNINGS
from .runner import Runner
from .utils import get_node_env
JSException = exception.JSException
RunTimeNotFoundError = exception.RunTimeNotFoundError
_logger = logging.getLogger("JSEval")
if not IS_WINDOWS:
    _DETACHED_PROCESS = 0
else:
    _DETACHED_PROCESS = subprocess.DETACHED_PROCESS


class AbstractRuntime:

    @abc.abstractmethod
    def eval(self, code: str = None):
        raise NotImplementedError()

    @abc.abstractmethod
    async def async_eval(self, code: str = None):
        raise NotImplementedError()

    @abc.abstractmethod
    def compile(self, source: str = None, suffix: str = None):
        raise NotImplementedError()

    def _eval(self, code: str = None, ignore_output=False):
        node = get_node_env()
        _cmd = [node, NO_WARNINGS]
        _input = Runner.program('eval', code)
        try:
            popen = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     universal_newlines=True, creationflags=_DETACHED_PROCESS)
        except Exception:
            raise RunTimeNotFoundError("Missing node environment")

        try:
            outs, errs = popen.communicate(input=_input)
        except Exception as e:
            _logger.error(e)
            popen.kill()
            outs, errs = popen.communicate()

        if popen.returncode != 0:
            raise JSException(outs)

        return self._extract_result(outs, ignore_output)

    async def _async_eval(self, code: str = None, ignore_output=False):
        node = get_node_env()
        _input = Runner.program('eval', code).encode("utf-8")
        try:
            process = await asyncio.create_subprocess_exec(
                node, NO_WARNINGS, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=_DETACHED_PROCESS
            )
        except Exception:
            raise RunTimeNotFoundError("Missing node environment")

        try:
            outs, errs = await process.communicate(input=_input)
        except Exception as e:
            _logger.error(e)
            process.kill()
            outs, errs = await process.communicate()

        outs = outs.decode("utf-8")
        if process.returncode != 0:
            raise JSException(outs)

        return self._extract_result(outs, ignore_output)

    @staticmethod
    def _extract_result(outs: str, ignore_output=False):
        _outs = outs.strip().split("\n")
        if not _outs[0]:
            return
        try:
            for out in _outs[:-2]:
                if not ignore_output:
                    print(out)
            if _outs[-2] == "JSEval_state: ok":
                try:
                    return json.loads(_outs[-1])
                except json.JSONDecodeError:
                    _logger.error("not supported this behaviour")
                    return None
            else:
                if not ignore_output:
                    print(_outs[-2])
                    print(_outs[-1])
        except IndexError:
            if not ignore_output:
                print(_outs[-1])


class AbstractContext:

    @abc.abstractmethod
    def call(self, *args, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    async def async_call(self, *args, **kwargs):
        raise NotImplementedError()

    def _call(self, func, args):
        node = get_node_env()
        _source = Runner.program('call', self._source, func, args)
        _path = self._make_temp_file(_source)
        _cmd = [node, NO_WARNINGS, _path]
        try:
            popen = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     universal_newlines=True, creationflags=_DETACHED_PROCESS)
        except Exception:
            os.remove(_path)
            raise RunTimeNotFoundError("Missing node environment")

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

    async def _async_call(self, func, args, async_js_func):
        node = get_node_env()
        if async_js_func:
            action = "async_call"
        else:
            action = "call"

        _input = Runner.program(action, self._source, func, args).encode("utf-8")
        try:
            process = await asyncio.create_subprocess_exec(
                node, NO_WARNINGS, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=_DETACHED_PROCESS
            )
        except Exception:
            raise RunTimeNotFoundError("Missing node environment")

        try:
            outs, errs = await process.communicate(input=_input)
        except Exception as e:
            _logger.error(e)
            process.kill()
            outs, errs = await process.communicate()

        outs = outs.decode("utf-8")
        if process.returncode != 0:
            raise JSException(outs)

        return self._extract_result(outs)

    @staticmethod
    def _extract_result(outs: str):
        _outs = outs.strip().split("\n")
        if not _outs[0]:
            return
        try:
            if _outs[-2] == "JSEval_state: ok":
                try:
                    return json.loads(_outs[-1])
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
