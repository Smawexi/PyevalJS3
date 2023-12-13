### 一个依赖node.js来执行js代码的库

----------------------

### 环境
**注意** 需要安装好node.js!!!

-----------------------------------

### 安装
```text
pip install pyevaljs3
```

-------------------------------

### 快速开始

```python
import pyevaljs3

js_code = "console.log(100); return 'ok';"
js_eval = pyevaljs3.JSEval()
js_eval.eval(js_code)
```

----------------------------------------

### API参考
**pyevaljs3.JSEval**  
- def compile(self, source: str = None, suffix: str = None):  
&ensp;&ensp; 编译javascript源代码  
&ensp;&ensp; :param source: 源代码字符串或要读取的文件路径  
&ensp;&ensp; :param suffix: js脚本文件名后缀(指定以什么模式执行), 默认是".js", 可选的值还有".cjs", ".mjs"等  
&ensp;&ensp; :return: Context  
- def eval(self, code: str = None):  
&ensp;&ensp; 执行javascript代码, 返回其结果(对于长字符串的情况，请使用compile)  

------------------------------

**pyevaljs3.Context**  
- def call(self, func, *args):  
&ensp;&ensp; 调用指定的函数, 返回其结果  
&ensp;&ensp; :param func: 函数名  
&ensp;&ensp; :param args: 函数的参数列表  

--------------------------------------

**pyevaljs3的模块级函数**  
- def compile_(source: str = None, mode: str = None) -> Context:    
&ensp;&ensp; 编译js源代码   
&ensp;&ensp; :param source: 源代码字符串或要读取的文件路径    
&ensp;&ensp; :param suffix: 执行模式, 默认以.js的行为去执行   
&ensp;&ensp; :return: Context    


- def eval_(code: str = None):  
&ensp;&ensp; 执行javascript代码, 返回其结果(对于长字符串的情况，请使用compile)  
&ensp;&ensp; :param code: js代码  

-----------------------------------

**欢迎各位使用此库, 有问题请提交issue**
