from stone.ast.expr import ASTList
from stone.exe.env import NestedEnv

class Postfix(ASTList):
    pass

class ParameterList(ASTList):
    def name(self, i):
        return self.child(i).token().text()

    def size(self):
        return self.num_children()

class DefStmnt(ASTList):
    def name(self):
        return self.child(0).token().text()
    
    def parameters(self):
        return self.child(1)

    def body(self):
        return self.child(2)

class Argument(Postfix):
    def size(self):
        return self.num_children()

class Function(object):
    def __init__(self, parameters, body, env):
        self._parameters = parameters
        self._body = body
        self._env = env

    def make_env(self):
        return NestedEnv(self._env)

    def body(self):
        return self._body

    def env(self):
        return self._env

    def parameters(self):
        return self._parameters

    def __str__(self):
        return "<function (%s)> %s" % (self.parameters(), self.body())

class Fun(ASTList):
    def parameters(self):
        return self.child(0)

    def body(self):
        return self.child(1)