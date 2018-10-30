import os

from stone.exe.interpreter import BasicInterpreter, FuncInterpreter
from . import get_source_path

def test_interpreter():
    with open(get_source_path("hello.stone"), "r") as fp:
        BasicInterpreter().main(fp)

def test_func_interpreter():
    with open(get_source_path("fib.stone"), "r") as fp:
        FuncInterpreter().main(fp)