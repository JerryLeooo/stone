from stone.common.exc import ParseException
from stone.ast.tree import ASTList, ASTLeaf
from stone.lexer.token import Token

# from chapter 17
class Parser(object):
    class Element(object):
        def parse(self, lexer, res):
            raise NotImplementedError
        def match(self, lexer):
            raise NotImplementedError

    class Tree(Element):
        def __init__(self, parser):
            self.parser = parser

        def parse(self, lexer, res):
            res.add(self.parser.parse(lexer))

        def match(self, lexer):
            return self.parser.match(lexer)

    class OrTree(Element):
        def __init__(self, parsers):
            self.parsers = parsers

        def parse(self, lexer, res):
            parser = self.choose(lexer)
            if parser is None:
                raise ParseException(lexer[0])
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
            self.parsers.append(parser)

    class Repeat(Element):
        def __init__(self, parser, once):
            self.parser = parser
            self.once = once

        def parse(self, lexer, res):
            while self.parser.match(lexer):
                ast_tree = self.parser.parse(lexer)
                if ast_tree.__class__ != ASTList or ast_tree.num_children() > 0:
                    res.append(ast_tree)
                if self.once:
                    break

        def match(self, lexer):
            return self.parser.match(lexer)

    class ATokn(Element):
        def __init__(self, type):
            if type is None:
                type = ASTLeaf.__class__
            self.factory = Factory.get(type, Token.__class__)

        def parse(self, lexer, res):
            t = lexer.read()
            if self.test(t):
                leaf = self.factory.make(t)
                res.append(t)
            else:
                raise ParseException

        def match(self, lexer):
            self.test(lexer[0])

        def test(self, t):
            raise NotImplementedError

    class IdToken(Element):
        def __init__(self, type, r):
            super(type)
            self.reserved = r if r else set()

        def test(self, t):
            return t.is_identifier() and not t.get_text() in reserved
        
    class NumToken(Element):
        def __init__(self, type):
            super(type)

        def test(self, t):
            return t.is_number()

    class StrToken(AToken):
        def __init__(self, type):
            super(type)

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
                        find(res, t)
                        return

            if len(self.tokens) > 0:
                raise ParseException(self.tokens[0] + " expected", t)
            else:
                raise ParseException(t)

        def find(self, res, t):
            res.add(ASTLeaf(t))

        def match(self, lexer):
            t = lexer[0]
            if t.is_identifier():
                for token in self.tokens:
                    if token == t.get_text():
                        return True

            return False

    class Skip(Leaf):
        def __init__(self, type):
            super(type)

        def find(self, res, t):
            pass

    class Precedence(object):
        def __init__(self, value, left_assoc):
            self.value = value
            self.left_assoc = left_assoc

    class Operators(object):
        def __init__(self):
            self.container = {}

        def add(self, name, prec, left_assoc):
            self.container[name] = Precedence(prec, left_assoc)

    class Expr(Element):
        def __init__(self, type, parser, operators):
            self.factory = Factory.get_for_astlist(type)
            self.ops = operators
            self.factor = parser

        def parse(self, lexer, res):
            right = self.factor.parse(lexer)
            while prec = self.next_operator(lexer) and prec != None:
                right = self.do_shift(lexer, right, prec.value)
            res.add(right)

        def do_shift(self, lexer, left, prec):
            l = [left, ASTLeaf(lexer.read())]

            right = factor.parse(lexer)
            while n = self.next_operator(lexer) and n != None and self.right_is_expr(prec, n):
                right = self.do_shift(lexer, right, n.value)

            l.append(right)
            return self.factory.make(l)

        def next_operator(self, lexer):
            t = lexer[0]
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
        def make0(self, arg):
            raise NotImplementedError

        def make(self, arg):
            try:
                self.make0(arg)
            except IllegalArgumentException as e:
                raise e
            except Exception as e:
                raise RuntimeError(e)

        def get_for_astlist(self, type):
            factory = self.get(type, List)
            if f is None:
                pass
