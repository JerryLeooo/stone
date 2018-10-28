import os
from stone.common.reader import LineNumberReader
from . import get_source_path

def test_reader():
    with open(get_source_path("hello.stone"), "r") as fp:
        reader = LineNumberReader(fp)

        reader.read_line()
        assert reader.line_no == 1

        line = reader.read_line()
        assert reader.get_line_number() == 2
        assert line == "i = 1\n"
