from stone.ast.expr import ASTList

class Postfix(ASTList):
    pass

class ParameterList(ASTList):
    def name(self, i):
        return self.child(i).token().get_text()

    def size(self):
        return self.num_children()

class DefStmnt(ASTList):
    def name(self):
        return self.child(0).token().get_text()

class Argument(Postfix):
    def size(self):
        return self.num_children()