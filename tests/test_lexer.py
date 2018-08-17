import os
from stone.lexer.lexer import Lexer
from stone.lexer.token import Token


def test_lexer_read():
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))

    with open("%s/hello.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)

        t = lexer.read()
        assert t.get_text() == "sum"

        t = lexer.read()
        assert t.get_text() == " =" # not right now, should do trim

def test_lexer():

    pwd = os.path.abspath(os.path.join(__file__, os.pardir))

    with open("%s/hello.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)

        result = []
        t = lexer.read()

        assert t.get_text() == "sum"

        while t != Token.EOF:
            result.append(t)
            t = lexer.read()

        assert len(result) == 30