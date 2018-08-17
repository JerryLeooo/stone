from stone.ast.tree import ASTTree, ASTList, ASTLeaf

class PrimaryExpr(ASTList):
    def create(self, tree):
        return tree.get(0) if tree.size() == 1 else PrimaryExpr(tree)

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
        return "(if " + self.condition() + " " + self.then_block() + " else " + self.else_block() + ")"

class WhileStmnt(ASTList):
    def condition(self):
        return self.child(0)

    def body(self):
        return self.child(1)

    def __str__(self):
        return "(while " + self.condition() + " " + self.body() + ")"

class NullStmnt(ASTList):
    pass

class StringLiteral(ASTLeaf):
    def value(self):
        return self.token().getText()

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