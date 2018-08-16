import os
from stone.common.reader import LineNumberReader

def test_reader():
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))

    with open("%s/hello.stone" % pwd, "r") as fp:
        reader = LineNumberReader(fp)

        reader.read_line()
        assert reader.current_line == 1

        assert reader.total_lines == 7

        line = reader.read_line()
        assert reader.get_line_number() == 2
        assert line == "i = 1\n"
