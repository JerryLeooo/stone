import os
from stone.lexer.lexer import Lexer
from stone.common.reader import LineNumberReader

def test_lexer():

    pwd = os.path.abspath(os.path.join(__file__, os.pardir))

    with open("%s/hello.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)

        result = []
        t = lexer.read()
        while t:
            result.append(t)
            t = lexer.read()

        assert len(result) == 17

