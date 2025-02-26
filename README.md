### 一个依赖node.js来执行js代码的库

----------------------

### 环境
**注意** 需要安装好node.js, 并添加好环境变量!!!

-----------------------------------

### 安装
```text
pip install pyevaljs3
```

-------------------------------

### 快速开始

```python
import pyevaljs3

js_code = "function f(args) {console.log(args); return 'ok';}; return f('args')"
result = pyevaljs3.eval_(js_code)
print(result) # 'ok'

js_code = "function f(arg1, arg2) {console.log(arg1, arg2); return arg1 + arg2;}"
ctx = pyevaljs3.compile_(js_code)
result = ctx.call('f', 'a', 'b')
print(result) # 'ab'

#另一钟传参方式
result = ctx.call('f', arg_list=['a', 'b'])
print(result) # 'ab'

# 调用js异步函数
js_code = "async function f(arg1, arg2) {console.log(arg1, arg2); return arg1 + arg2;}"
ctx = pyevaljs3.compile_(js_code)
async def main():
    result = await ctx.async_call('f', "a", "b", async_js_func=True)
    return result

import asyncio
result = asyncio.run(main())
print(result) # 'ab'
```

----------------------------------------

### API参考
**pyevaljs3.JSEval**  
- def compile(self, source: str = None, suffix: str = None):  
&ensp;&ensp; 编译javascript源代码  
&ensp;&ensp; :param source: 源代码字符串或要读取的文件路径  
&ensp;&ensp; :param suffix: js脚本文件名后缀(指定以什么模式执行), 默认是".js", 可选的值还有".cjs", ".mjs"等  
&ensp;&ensp; :return: Context  


- def eval(self, code: str = None, ignore_output=False):  
&ensp;&ensp; 执行javascript代码, 返回其结果


- async def async_eval(self, code: str = None, ignore_output=False):  
&ensp;&ensp; 执行javascript代码, 返回其结果(异步版本的eval)

------------------------------

**pyevaljs3.Context**  
- def call(self, func, *args, arg_list: List = None):  
&ensp;&ensp; 调用指定的函数, 返回其结果(若指定了arg_list, 优先使用它作为函数参数)  
&ensp;&ensp; :param func: 函数名  
&ensp;&ensp; :param args: 函数的参数列表  
&ensp;&ensp; :param arg_list: 函数的参数列表


- async def async_call(self, func, *args, arg_list: List = None, async_js_func: bool = False):  
&ensp;&ensp; 调用指定的函数, 返回其结果(若指定了arg_list, 优先使用它作为函数参数), 参数解释同call  
&ensp;&ensp; :param async_js_func: 调用的js函数是否是异步js函数  

--------------------------------------

**pyevaljs3的模块级函数**  
- def compile_(source: str = None, mode: str = None) -> Context:    
&ensp;&ensp; 编译js源代码   
&ensp;&ensp; :param source: 源代码字符串或要读取的文件路径    
&ensp;&ensp; :param mode: 执行模式, 默认以.js的行为去执行   
&ensp;&ensp; :return: Context    


- def eval_(code: str = None, ignore_output=False):   
&ensp;&ensp; 执行javascript代码, 返回其结果  
&ensp;&ensp; :param code: js代码  
&ensp;&ensp; :param ignore_output: 是否忽略执行过程中的输出, 若为True则仅返回其结果, 默认不忽略(False)  


- async def async_eval(code: str = None, ignore_output=False):  
&ensp;&ensp; 执行javascript代码, 返回其结果, 参数解释同eval_, 异步版本的eval_  

-----------------------------------

#### 使用自定义版本的node

- 通过设置坏境变量来使用自定义版本的node, 只需设置NODE_PATH、NODE坏境变量即可  
```python
import os
# 优先级最高
os.environ['NODE_PATH'] = '/path/to/node.exe'
# 或者
# 优先级其次
os.environ['NODE'] = '/path/to/node.exe'
```

