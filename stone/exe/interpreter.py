import sys
from stone.exe.env import BasicEnv
from stone.lexer.lexer import Lexer
from stone.lexer.token import Token
from stone.ast.expr import NullStmnt
from stone.exe.evaluator import BasicEvaluator
from stone.parser.basic_parser import BasicParser, FuncParser, ClosureParser
from stone.exe.env import NestedEnv
from stone.exe.native import Natives

class BasicInterpreter(object):
    def main(self, fp):
        self.run(BasicParser(), BasicEnv(), fp)

    def run(self, parser, env, fp):
        lexer = Lexer(fp)
        while lexer.peek(0) != Token.EOF:
            t = parser.parse(lexer)
            if not isinstance(t, NullStmnt):
                r = t.eval(env)
                print("=> ", t, "//", r, t.__class__)

class FuncInterpreter(BasicInterpreter):
    def main(self, fp):
        self.run(FuncParser(), NestedEnv(), fp)

class ClosureInterpreter(BasicInterpreter):
    def main(self, fp):
        self.run(ClosureParser(), NestedEnv(), fp)

class NativeInterapreter(BasicInterpreter):
    def main(self, fp):
        self.run(ClosureParser(), Natives().environment(NestedEnv()), fp)