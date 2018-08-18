from stone.parser.parser import Parser, Operators
from stone.ast.expr import ASTTree, ASTLeaf, ASTList 
from stone.ast.expr import NumberLiteral, BinaryExpr, StringLiteral, PrimaryExpr, Name, BlockStmnt, IfStmnt, WhileStmnt, NullStmnt, NegativeExpr
from stone.lexer.token import Token

rule = Parser.rule

class BasicParser(object):
    def __init__(self):
        self.reserved = set()
        self.operators = Operators()
        self.primary = (
            rule(PrimaryExpr).my_or(
                Parser().sep("(").ast(Parser()).sep(")"),
                Parser().number(NumberLiteral),
                Parser().identifier(self.reserved, Name),
                Parser().string(StringLiteral)
            )
        )
        self.factor = Parser().my_or(rule(NegativeExpr).sep("-").ast(self.primary), self.primary)
        self.expr = Parser().expression(self.factor, self.operators, BinaryExpr)
        self.block = (
            rule(BlockStmnt)
            .sep("{")
                .option(Parser())
                .repeat(Parser().sep(";", Token.EOL).option(Parser()))
            .sep("}")
        )
        self.simple = rule(PrimaryExpr).ast(self.expr)
        self.statement = Parser().my_or(
            rule(IfStmnt).sep("if").ast(self.expr).ast(self.block)
                .option(Parser().sep("else").ast(self.block)),
            rule(WhileStmnt).sep("while").ast(self.expr).ast(self.block),
            self.simple
        )
        self.program = Parser().my_or(
            self.statement, rule(NullStmnt)
        ).sep(";", Token.EOL)

        self.init()

    def init(self):
        self.reserved.add(";")
        self.reserved.add("}")
        self.reserved.add(Token.EOL)

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
