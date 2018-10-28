import os
from stone.lexer.lexer import Lexer
from stone.parser.basic_parser import BasicParser
from stone.parser.parser import Parser
from stone.lexer.token import Token
from stone.ast.expr import Name, WhileStmnt, BlockStmnt
import sys, traceback
from . import get_source_path

bp = BasicParser()

def test_more_parser():
    with open(get_source_path("more.stone"), "r") as fp:
        lexer = Lexer(fp)
        bp = BasicParser()
        while lexer.peek(0) != Token.EOF:
            ast = bp.parse(lexer)
            print(ast)
