from stone.exe.interpreter import NativeInterapreter
from . import get_source_path

def test_natives():
    with open(get_source_path("native_fib.stone"), "r") as fp:
        NativeInterapreter().main(fp)