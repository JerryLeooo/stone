from stone.parser.parser import Parser, Operators
from stone.ast.expr import NumberLiteral, BinaryExpr, StringLiteral, PrimaryExpr, Name, BlockStmnt, IfStmnt, WhileStmnt, NullStmnt, NegativeExpr
from stone.lexer.token import Token
from stone.ast.func import ParameterList, DefStmnt, Argument, Fun
from stone.ast.classes import ClassBody, ClassStmnt, Dot

rule = Parser.rule

class BasicParser(object):
    def __init__(self):
        self.reserved = set()
        self.operators = Operators()
        self.init()

        self.expr0 = Parser(name="expr0")
        self.primary = (
            rule(PrimaryExpr, name="primary").my_or(
                Parser(name="expr").sep("(").ast(self.expr0).sep(")"),
                Parser(name="number").number(NumberLiteral),
                Parser(name="identifier").identifier(self.reserved, Name),
                Parser(name="string").string(StringLiteral)
            )
        )
        self.factor = Parser(name="NegativeExpr or primary").my_or(
            rule(NegativeExpr, "negative").sep("-").ast(self.primary), self.primary
        )
        self.expr = self.expr0.expression(self.factor, self.operators, BinaryExpr)

        self.statement0 = Parser(name="statement0")
        self.block = (
            rule(BlockStmnt, name="BlockStmnt")
            .sep("{")
                .option(self.statement0)
                .repeat(Parser(name="repeat").sep(";", Token.EOL).option(self.statement0))
            .sep("}")
        )
        self.simple = rule(PrimaryExpr, name="simple").ast(self.expr)
        self.statement = self.statement0.my_or(
            rule(IfStmnt, name="if").sep("if").ast(self.expr).ast(self.block)
                .option(Parser(name="else").sep("else").ast(self.block)),
            rule(WhileStmnt, name="while").sep("while").ast(self.expr).ast(self.block),
            self.simple
        )
        self.program = Parser(name="program").my_or(
            self.statement, rule(NullStmnt, name="null statement")
        ).sep(";", Token.EOL)
        

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

class FuncParser(BasicParser):

    def __init__(self):
        super().__init__()
        self.reserved.add(")")
        self.param = Parser(name="param").identifier(self.reserved)
        self.params = rule(ParameterList, name="params").ast(self.param).repeat(
            rule(name="param??").sep(",").ast(self.param)
        )

        self.param_list = Parser(name="param list").sep("(").maybe(self.params).sep(")")
        self.define = rule(DefStmnt, name="define").sep("def").identifier(self.reserved).ast(self.param_list).ast(self.block)
        self.args = rule(Argument, name="argument").ast(self.expr).repeat(rule(name="repeat expr").sep(",").ast(self.expr))
        self.postfix = Parser(name="postfix").sep("(").maybe(self.args).sep(")")

        self.primary = self.primary.repeat(self.postfix)
        self.simple = self.simple.option(self.args)
        self.program = self.program.insert_choice(self.define)

class ClosureParser(FuncParser):
    def __init__(self):
        super().__init__()
        self.primary.insert_choice(rule(Fun, name="fun").sep("fun").ast(self.param_list).ast(self.block))

class ClassParser(ClosureParser):
    def __init__(self):
        super().__init__()
        self.member = Parser(name="member").my_or(self.define, self.simple)
        self.class_body = Parser(ClassBody, name="class_body").sep("{").option(self.member).repeat(Parser().sep(";", Token.EOL).option(self.member)).sep("}")
        self.def_class = Parser(ClassStmnt, name="def_class").sep("class").identifier(self.reserved).option(Parser().sep("extends").identifier(self.reserved)).ast(self.class_body)
        
        self.postfix.insert_choice(Parser(Dot, name="dot").sep(".").identifier(self.reserved))
        self.program.insert_choice(self.def_class)
