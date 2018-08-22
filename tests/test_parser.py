import os
from stone.lexer.lexer import Lexer
from stone.parser.basic_parser import BasicParser
from stone.parser.parser import Parser
from stone.lexer.token import Token
from stone.ast.expr import Name, WhileStmnt, BlockStmnt

import sys, traceback

bp = BasicParser()
pwd = os.path.abspath(os.path.join(__file__, os.pardir))

def test_more_parser():
    with open("%s/more.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        bp = BasicParser()
        while lexer.peek(0) != Token.EOF:
            ast = bp.parse(lexer)
            print(ast)
