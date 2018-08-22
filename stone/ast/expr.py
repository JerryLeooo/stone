class ASTTree(object):
    def child(self, i):
        raise NotImplementedError

    def num_children(self):
        raise NotImplementedError

    def location(self):
        raise NotImplementedError

    def children(self):
        raise NotImplementedError

    def iterator(self):
        return self.children()

class ASTLeaf(ASTTree):

    def __init__(self, t):
        self.token = t

    def child(self, i):
        raise IndexError

    def num_children(self):
        return 0

    def loation(self):
        return "at line %s" % self.token.get_line_number()

    def get_token(self):
        return self.token

    def __str__(self):
        return self.get_token().get_text()

class ASTList(ASTTree):

    def __init__(self, l):
        self._children = l

    def child(self, i):
        self._children[i]

    def num_children(self):
        return len(self._children)

    def children(self):
        return iter(self._children)

    def location(self):
        for t in self._children:
            s = t.location()
            if s:
                return s

        return None

    def __str__(self):
        return "(" + " ".join([str(c) for c in list(self.children())]) + ")"

class PrimaryExpr(ASTList):
    
    @classmethod
    def create(self, tree):
        return tree[0] if len(tree) == 1 else PrimaryExpr(tree)

class NegativeExpr(ASTList):
    def operand(self):
        return self.child(0)

    def __str__(self):
        return "-" + self.operand()

class BlockStmnt(ASTList):
    pass

class IfStmnt(ASTList):
    def condition(self):
        return self.child(0)

    def then_block(self):
        return self.child(0)

    def else_block(self):
        return self.child(2) if self.num_children() > 2 else None

    def __str__(self):
        return "(if %s %s else %s )" % (
            self.condition(), self.then_block(), self.else_block())

class WhileStmnt(ASTList):

    def __init__(self, l):
        super().__init__(l)

    def condition(self):
        return self.child(0)

    def body(self):
        return self.child(1)

    def __str__(self):
        print(self.condition())
        print(self.body())
        return "(while %s {%s})" % (self.condition(), self.body())

class NullStmnt(ASTList):
    pass

class StringLiteral(ASTLeaf):
    def value(self):
        return self.get_token().get_text()

class NumberLiteral(ASTLeaf):
    def __init__(self, t):
        super().__init__(t)

    def value(self):
        return self.get_token().get_number()

class Name(ASTLeaf):
    
    def __init__(self, t):
        super().__init__(t)

    def name(self):
        return self.get_token().get_text()

class BinaryExpr(ASTList):
    
    def __init__(self, t):
        super().__init__(t)

    def left(self):
        return self.child(0)

    def operator(self):
        return self.child(1).token.get_text()

    def right(self):
        return self.child(2)