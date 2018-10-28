import sys
from stone.parser.basic_parser import BasicParser
from stone.exe.env import BasicEnv
from stone.lexer.lexer import Lexer
from stone.lexer.token import Token
from stone.ast.expr import NullStmnt
from stone.exe.evaluator import BasicEvaluator

class BasicInterpreter(object):
    def main(self, fp):
        self.run(BasicParser(), BasicEnv(), fp)

    def run(self, basic_parser, env, fp):
        lexer = Lexer(fp)
        while lexer.peek(0) != Token.EOF:
            t = basic_parser.parse(lexer)
            if not isinstance(t, NullStmnt):
                print("???", t)
                r = t.eval(env)
                print("=> ", r)