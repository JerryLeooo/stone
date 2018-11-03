from stone.ast.expr import ASTList
from stone.exe.env import NestedEnv
from stone.common.exc import StoneException
import inspect

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

class NativeFunction(object):
    def __init__(self, n, m):
        self.name = n
        self.method = m
        self.num_params = len(inspect.getargspec(m).args)

    def num_of_parameters(self):
        return self.num_params

    def invoke(self, args, tree):
        try:
            return self.method(args)
        except:
            raise StoneException("bad native function call: %s" % self.name, tree)

    