from setuptools import setup, find_packages
from pyevaljs3.__version__ import version

NAME = 'pyevaljs3'
URL = "https://github.com/Smawexi/PyevalJS3"
EMAIL = '1281722462@qq.com'
AUTHOR = 'Samwe'
REQUIRES_PYTHON = '>=3.6.0'
DESCRIPTION = '一个依赖node.js来执行js代码的python库'
LONG_DESCRIPTION = open('README.md', encoding="utf-8").read()

setup(
    name=NAME,
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(where=".", exclude=('tests',)),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires=">= 3.6.0"
)
