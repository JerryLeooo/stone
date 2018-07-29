from stone.parser.parser improt Parser

class BasicParser(Parser):
    def rule(self):
        pass

    def parse(self, lexer):
        pass

    def number(self):
        pass

    def identifier(self, reversed):
        pass

    def string(self):
        pass

    def token(self, pattern):
        pass

    def sep(self):
        pass

    def ast(self, parser):
        pass

    def option(self, parser):
        pass

    def maybe(self, parser):
        pass

    def op_or(self, parser):
        pass

    def repeat(self, parser):
        pass

    def expression(self, parser, op):
        pass

    def reset(self):
        pass

    def insertChoice(self, parser):
        pass

class BasicParser(object):
    reserved = {}
    opreators = Operators()
    expr0 = rule()
    primary = rule(PrimaryExpr)


