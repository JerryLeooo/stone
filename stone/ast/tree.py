class ASTTree(object):
    def child(self, i):
        raise NotImplemented

    def num_children(self):
        raise NotImplemented

    def location(self):
        raise NotImplemented

    def children(self):
        raise NotImplemented

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
        return self.token.get_text()

class ASTList(ASTTree):

    def __init__(self, l):
        self.children = l

    def child(self, i):
        self.children[i]

    def num_children(self):
        return len(self.children)

    def children(self):
        return self.children.iterator()

    def location(self):
        for t in self.children:
            s = t.location()
            if s:
                return s

        return None

    def __str__(self):
        return " ".join(self.children)

class NumberLiteral(ASTLeaf):
    def value(self):
        return self.get_token().get_number()

class Name(ASTLeaf):
    def name(self):
        return self.get_token().get_number()

class BinaryExpr(ASTList):
    def left(self):
        return self.child(0)

    def operator(self):
        return ASTLeaf(self.child(1)).token().get_text()

    def right(self):
        return self.child(1)
