import os

from stone.env.interpreter import BasicInterpreter
from . import get_source_path

def test_interpreter():
    with open(get_source_path("hello.stone"), "r") as fp:
        BasicInterpreter().main(fp)