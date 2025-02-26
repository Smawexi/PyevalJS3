NODE_CALL = '{_source};var __result = {func}.apply(this, {args});if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}}'


NODE_EVAL = 'var __result = (() => {{{code}}})();if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}};'


NODE_ASYNC_CALL = '{_source};{func}.apply(this, {args}).then(__result => {{if (__result !== undefined) {{console.log("JSEval_state: ok");console.log(JSON.stringify(__result));}}}});'
