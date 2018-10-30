from stone.ast.expr import ASTList
from stone.exe.env import NestedEnv

class Postfix(ASTList):
    pass

class ParameterList(ASTList):
    def name(self, i):
        return self.child(i).get_token().get_text()

    def size(self):
        return self.num_children()

class DefStmnt(ASTList):
    def name(self):
        return self.child(0).get_token().get_text()
    
    def parameters(self):
        return self.child(1)

    def body(self):
        return self.child(2)

class Argument(Postfix):
    def size(self):
        return self.num_children()

class Function(object):
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env

    def make_env(self):
        return NestedEnv(self.env)
