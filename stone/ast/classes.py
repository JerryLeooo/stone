from stone.ast.expr import ASTList
from stone.ast.func import Postfix

class ClassBody(ASTList):
    pass

class ClassStmnt(ASTList):
    def name(self):
        return self.child(0).token().text()

    def super_class(self):
        if self.num_children() < 3:
            return None
        else:
            return self.child(1).token().text()

    def body(self):
        return self.child(self.num_children() - 1)

    def __str__(self):
        parent = self.super_class()
        if parent is None:
            parent = "*"

        return "(class %s %s %s)" % (self.name(), parent, self.body())

class Dot(Postfix):
    def name(self):
        return self.child(0).token().text()
    def __str__(self):
        return "." + self.name()

class ClassInfo(object):
    def __init__(self, class_stmnt, env):
        self.definition = class_stmnt
        self.environment = env

        obj = env.get(class_stmnt.super_class())
        if obj is None:
            self.sc = None
        elif isinstance(obj, ClassInfo):
            self.sc = obj
        else:
            raise StoneException("unknown super class: %s" % (class_stmnt.super_class()), class_stmnt)

    def name(self):
        return self.definition.name()

    def super_class(self):
        return self.sc

    def body(self):
        return self.definition.body()

    def environment(self):
        return self.environment

    def __str__(self):
        return "<class %s>" % self.name()

class StoneObject(object):

    class AccessException(Exception):
        pass

    def __init__(self, env):
        self.environment = env

    def read(self, member):
        return self.get_env(member).get(member)

    def write(self, member, value):
        self.get_env(member).put_new(member, value)

    def get_env(self, member):
        e = self.environment.where(member)
        if not e is None and e == self.environment:
            return e
        else:
            raise AccessException
