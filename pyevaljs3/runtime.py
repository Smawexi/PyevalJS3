import subprocess
import logging
import json
import exception
import abc
JSException = exception.JSException
_logger = logging.getLogger("JSEval")


class AbstractRuntime:

    @abc.abstractmethod
    def eval(self, code: str = None):
        raise NotImplementedError()

    @abc.abstractmethod
    def compile(self, source: str = None, suffix: str = None):
        raise NotImplementedError()

    def _eval(self, code: str = None):
        _cmd = [
            "node",
            "-e",
            f'var __result = (() => {{{code}}})();if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}};'
        ]
        popen = subprocess.Popen(_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 universal_newlines=True, creationflags=subprocess.DETACHED_PROCESS)
        try:
            outs, errs = popen.communicate()
        except Exception as e:
            _logger.error(e)
            popen.kill()
            outs, errs = popen.communicate()

        if popen.returncode != 0:
            raise JSException(outs)

        return self._extract_result(outs)

    @staticmethod
    def _extract_result(outs: str):
        if not outs.strip().split("\n")[0]:
            return
        try:
            for out in outs.strip().split("\n")[:-2]:
                print(out)
            if outs.strip().split("\n")[-2] == "JSEval_state: ok":
                return json.loads(outs.strip().split()[-1])
            else:
                print(outs.strip().split()[-2])
                print(outs.strip().split()[-1])
        except IndexError:
            print(outs.strip().split("\n")[-1])
