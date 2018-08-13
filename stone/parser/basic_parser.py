from stone.parser.parser import Parser, Operators
from stone.ast.tree import ASTTree, ASTLeaf, ASTList 
from stone.ast.expr import NumberLiteral, BinaryExpr, StringLiteral, PrimaryExpr, Name, BlockStmnt, IfStmnt, WhileStmnt, NullStmnt, NegativeExpr
from stone.lexer.token import Token

rule = Parser.rule

class BasicParser(object):
    def __init__(self):
        self.reserved = set(";", "}", Token.EOL)
        self.operators = Operators()
        self.expr0 = Parser.rule()
        self.primary = (rule(PrimaryExpr)
                        .my_or(rule().sep("(").ast(self.expr0).sep(")"),
                            rule().number(NumberLiteral),
                            rule().identifier(Name, self.reserved),
                            rule().string(StringLiteral)
                           )
                       )
        self.factor = rule().my_or(rule(NegativeExpr).sep("-").ast(self.primary), self.primary)
        self.expr = self.expr0.expression(BinaryExpr, self.factor, self.operators)
        self.statement0 = rule()
        self.block = (rule(BlockStmnt).sep("{")
                      .option(self.statement0)
                      .repeat(rule().sep(";", Token.EOL).option(self.statement0))
                      .sep("}")
                     )
        self.simple = rule(self.primary).ast(self.expr)
        self.statement = self.statement0.my_or(
            rule(IfStmnt).sep("if").ast(self.expr).ast(self.block)
                .option(rule().sep("else").ast(self.block)),
            rule(WhileStmnt).sep("while").ast(self.expr).ast(self.block),
            self.simple
        )
        self.program = rule().my_or(self.statement,
                                 rule(NullStmnt)).sep(";", Token.EOL)
        self.init_operator()

    def init_operator(self):
        self.operators.add("=", 1, Operators.RIGHT)
        self.operators.add("==", 2, Operators.LEFT)
        self.operators.add(">", 2, Operators.LEFT)
        self.operators.add("<", 2, Operators.LEFT)
        self.operators.add("+", 3, Operators.LEFT)
        self.operators.add("-", 3, Operators.LEFT)
        self.operators.add("*", 4, Operators.LEFT)
        self.operators.add("/", 4, Operators.LEFT)
        self.operators.add("%", 4, Operators.LEFT)

    def parse(self, lexer):
        return self.program.parse(lexer)
