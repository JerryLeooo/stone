# from chapter 17
class Parser(object):
    class Element(object):
        def parse(lexer, res):
            raise NotImplementedError
        def match(lexer):
            raise NotImplementedError

    class Tree(Element):
        def __init__(parser):
            self.parser = parser

        def parse(lexer, res):
            res.add(self.parser.parse(lexer))

        def match(lexer):
            return self.parser.match(lexer)
