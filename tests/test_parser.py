import os
from stone.lexer.lexer import Lexer
from stone.parser.basic_parser import BasicParser
from stone.parser.parser import Parser
from stone.lexer.token import Token
from stone.ast.expr import Name, WhileStmnt, BlockStmnt
'''
def test_identifier_parse():
    bp = BasicParser()
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))
    with open("%s/simple.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        id_result = Parser().identifier(set([";", "}", Token.EOL]), Name).parse(lexer)
        assert(id_result.name() == "sum")

def test_primary_parse():
    bp = BasicParser()
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))
    with open("%s/simple.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        primary_result = bp.primary.parse(lexer)
        assert(primary_result.name() == "sum")

def test_expr_parse():
    bp = BasicParser()
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))
    with open("%s/simple.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        expr_result = bp.expr.parse(lexer)
        print(expr_result)
'''

'''
def test_while_parse():
    bp = BasicParser()
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))
    with open("%s/while.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        while_result = Parser.rule(WhileStmnt).sep("while").ast(bp.expr).ast(bp.block).parse(lexer)
        print(while_result)
'''

def test_block_parse():
    bp = BasicParser()
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))
    with open("%s/block.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)

        parser = (Parser.rule(BlockStmnt)
            .sep("{")
                .option(Parser())
                .repeat(Parser().sep(";", Token.EOL).option(Parser()))
            .sep("}")
        )

        print("elements", parser.elements, parser)
        
        print("result", parser.parse(lexer))

'''
def test_parser():
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))

    with open("%s/more.stone" % pwd, "r") as fp:
        lexer = Lexer(fp)
        bp = BasicParser()
        while lexer.peek(0) != Token.EOF:
            ast = bp.parse(lexer)
            print(lexer.line_no, ast)
'''