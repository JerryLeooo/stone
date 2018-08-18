# from chapter 17
from stone.common.exc import ParseException
from stone.ast.expr import ASTList, ASTLeaf, ASTTree
from stone.lexer.token import Token

class Element(object):
    def parse(self, lexer, res):
        raise NotImplementedError
    def match(self, lexer):
        raise NotImplementedError

class Tree(Element):
    def __init__(self, parser):
        self.parser = parser

    def parse(self, lexer, res):
        res.append(self.parser.parse(lexer))

    def match(self, lexer):
        return self.parser.match(lexer)

class OrTree(Element):
    def __init__(self, parsers):
        self.parsers = parsers

    def parse(self, lexer, res):
        parser = self.choose(lexer)
        if parser is None:
            raise ParseException(lexer.peek(0).get_text())
        else:
            res.append(parser.parse(lexer))

    def match(self, lexer):
        return self.choose(lexer) != None

    def choose(self, lexer):
        for parser in self.parsers:
            if parser.match(lexer):
                return parser

        return None

    def insert(self, parser):
        self.parsers = [parser] + self.parsers

class Repeat(Element):
    def __init__(self, parser, only_once):
        self.parser = parser
        self.only_once = only_once

    def parse(self, lexer, res):
        while self.parser.match(lexer):
            ast_tree = self.parser.parse(lexer)
            if ast_tree.__class__ != ASTList or ast_tree.num_children() > 0:
                res.append(ast_tree)
            if self.only_once:
                break

    def match(self, lexer):
        return self.parser.match(lexer)

class AToken(Element):
    def __init__(self, clazz):
        if clazz is None:
            clazz = ASTLeaf
        self.factory = Factory.get(clazz, Token)

    def parse(self, lexer, res):
        t = lexer.read()
        if self.test(t):
            leaf = self.factory.make(t)
            res.append(leaf)
        else:
            raise ParseException(t)

    def match(self, lexer):
        return self.test(lexer.peek(0))

    def test(self, t):
        raise NotImplementedError

class IdToken(AToken):
    def __init__(self, clazz, r):
        super().__init__(clazz)
        self.reserved = r if r else set()

    def test(self, t):
        r = t.is_identifier() and not t.get_text() in self.reserved
        return r

class NumToken(AToken):
    def test(self, t):
        return t.is_number()

class StrToken(AToken):
    def test(self, t):
        return t.is_string()

class Leaf(Element):
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self, lexer, res):
        t = lexer.read()
        if t.is_identifier():
            for token in self.tokens:
                if token == t.get_text():
                    self.find(res, t)
                    return

        if len(self.tokens) > 0:
            raise ParseException(self.tokens[0] + " expected", t)
        else:
            raise ParseException(t)

    def find(self, res, t):
        res.append(ASTLeaf(t))

    def match(self, lexer):
        t = lexer.peek(0)
        if t.is_identifier():
            for token in self.tokens:
                if token == t.get_text():
                    return True

        return False

class Skip(Leaf):
    def find(self, res, t):
        pass

class Precedence(object):
    def __init__(self, value, left_assoc):
        self.value = value
        self.left_assoc = left_assoc

class Operators(dict):

    LEFT = True
    RIGHT = False

    def add(self, name, prec, left_assoc):
        self[name] = Precedence(prec, left_assoc)

class Expr(Element):
    def __init__(self, clazz, parser, operators):
        self.factory = Factory.get_for_astlist(clazz)
        self.ops = operators
        self.factor = parser

    def parse(self, lexer, res):
        right = self.factor.parse(lexer)
        prec = self.next_operator(lexer)
        while prec != None:
            right = self.do_shift(lexer, right, prec.value)
            prec = self.next_operator(lexer)
        res.append(right)

    def do_shift(self, lexer, left, prec):
        l = [left, ASTLeaf(lexer.read())]

        right = self.factor.parse(lexer)
        n = self.next_operator(lexer)
        while n != None and self.right_is_expr(prec, n):
            right = self.do_shift(lexer, right, n.value)
            n = self.next_operator(lexer)

        l.append(right)
        return self.factory.make(l)

    def next_operator(self, lexer):
        t = lexer.peek(0)
        if t.is_identifier():
            return self.ops.get(t.get_text())
        else:
            return None

    def right_is_expr(self, prec, next_prec):
        if next_prec.left_assoc:
            return prec < next_prec.value
        else:
            return prec <= next_prec.value

    def match(self, lexer):
        return self.factor.match(lexer)

class Factory(object):

    factory_name = 'create'

    def make0(self, arg):
        raise NotImplementedError

    def make(self, arg):
        try:
            return self.make0(arg)
        except Exception as e:
            raise RuntimeError(e)

    @classmethod
    def get_for_astlist(cls, clazz):
        factory = cls.get(clazz, list)
        if factory is None:
            def make0(arg):
                assert isinstance(arg, list)
                if len(arg) == 1:
                    return arg[0]
                else:
                    return ASTList(arg)

            factory = Factory()
            factory.make0 = make0

        return factory

    @classmethod
    def get(cls, clazz, arg_type):

        if not clazz:
            return None

        func = getattr(clazz, cls.factory_name, None)

        factory = cls()

        if func:
            factory.make0 = lambda arg: func(arg)
        else:
            factory.make0 = lambda arg: clazz(arg)

        return factory

class Parser(object):
    def __init__(self, arg = None):
        if isinstance(arg, Parser):
            self.elements = arg.elements
            self.factory = arg.factory
        else:
            self.reset(arg)

    def parse(self, lexer):
        results = []
        for e in self.elements:
            e.parse(lexer, results)

        return self.factory.make(results)

    def match(self, lexer):
        if len(self.elements) == 0:
            return True

        e = self.elements[0]
        return e.match(lexer)

    @classmethod
    def rule(cls, clazz = None):
        return cls(clazz)

    def reset(self, clazz = None):
        self.elements = []
        self.factory = Factory.get_for_astlist(clazz)
        return self

    def number(self, clazz):
        self.elements.append(NumToken(clazz))
        return self

    def identifier(self, reserved, clazz = None):
        self.elements.append(IdToken(clazz, reserved))
        return self

    def string(self, clazz = None):
        self.elements.append(StrToken(clazz))
        return self

    def token(self, *strings):
        self.elements.append(Leaf(strings))
        return self

    def sep(self, *strings):
        self.elements.append(Skip(strings))
        return self

    def ast(self, parser):
        self.elements.append(Tree(parser))
        return self

    def my_or(self, *parsers):
        self.elements.append(OrTree(parsers))
        return self

    def maybe(self, parser):
        p2 = Parser(parser)
        p2.reset()
        self.elements.append(OrTree([parser, p2]))
        return self

    def option(self, parser):
        self.elements.append(Repeat(parser, True))
        return self

    def repeat(self, parser):
        self.elements.append(Repeat(parser, False))
        return self

    def expression(self, sub_exp_parser, operators, clazz=None):
        self.elements.append(Expr(clazz, sub_exp_parser, operators))
        return self