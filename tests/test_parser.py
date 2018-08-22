import os
from stone.lexer.lexer import Lexer
from stone.parser.basic_parser import BasicParser
from stone.parser.parser import Parser
from stone.lexer.token import Token
from stone.ast.expr import Name, WhileStmnt, BlockStmnt

import sys, traceback

bp = BasicParser()
pwd = os.path.abspath(os.path.join(__file__, os.pardir))

# def test_identifier_parse():
#     bp = BasicParser()
#     pwd = os.path.abspath(os.path.join(__file__, os.pardir))
#     with open("%s/simple.stone" % pwd, "r") as fp:
#         lexer = Lexer(fp)
#         id_result = Parser().identifier(set([";", "}", Token.EOL]), Name).parse(lexer)
#         assert(id_result.name() == "sum")
# 
# def test_primary_parse():
#     bp = BasicParser()
#     pwd = os.path.abspath(os.path.join(__file__, os.pardir))
#     with open("%s/simple.stone" % pwd, "r") as fp:
#         lexer = Lexer(fp)
#         while lexer.peek(0) != Token.EOF:
#             bp.primary.parse(lexer)
# 
# def test_expr_parse():
#     with open("%s/expr.stone" % pwd, "r") as fp:
#         lexer = Lexer(fp)
#         bp.expr.parse(lexer)
# 
# def test_simple_parse():
#     with open("%s/expr.stone" % pwd, "r") as fp:
#         lexer = Lexer(fp)
#         bp.simple.parse(lexer)
# 
# def test_factor_parse():
#     with open("%s/factor.stone" % pwd, "r") as fp:
#         lexer = Lexer(fp)
#         bp.factor.parse(lexer)
# 
# def test_while_parse():
#     with open("%s/while.stone" % pwd, "r") as fp:
#         lexer = Lexer(fp)
#         while lexer.peek(0) != Token.EOF:
#             ast = bp.statement.parse(lexer)

def test_more_parser():
    with open("%s/more.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        bp = BasicParser()
        while lexer.peek(0) != Token.EOF:
            ast = bp.parse(lexer)
            print(lexer.line_no, ast)

def test_if_parser():
    with open("%s/if.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        bp = BasicParser()
        while lexer.peek(0) != Token.EOF:
            ast = bp.parse(lexer)
            print(lexer.line_no, ast)