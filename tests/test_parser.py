import os
from stone.lexer.lexer import Lexer
from stone.parser.basic_parser import BasicParser
from stone.lexer.token import Token

def test_parser():
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))

    with open("%s/more.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        bp = BasicParser()
        while lexer.peek(0) != Token.EOF:
            print(lexer.peek(0).get_text())
            ast = bp.parse(lexer)
            print("ast", ast.get_token())

    assert False