from stone.exe.interpreter import ClassInterpreter
from . import get_source_path

def test_class_interpreter():
    with open(get_source_path("class.stone"), "r") as fp:
        ClassInterpreter().main(fp)