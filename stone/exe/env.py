
from abc import ABCMeta

class Environment(object):

    __metaclass__ = ABCMeta
     
    def put(self, name, value):
        pass

    def get(self, name):
        pass

    def all(self):
        pass

class BasicEnv(Environment):
    def __init__(self):
        self.values = {}

    def put(self, name, value):
        self.values[name] = value

    def get(self, name):
        return self.values.get(name)

    def all(self):
        return self.values

class NestedEnv(Environment):
    def __init__(self, e = None):
        self.values = {}
        self.outer = e

    def set_outer(self, e):
        self.outer = e

    def get(self, name):
        v = self.values.get(name)
        if v == None and self.outer != None:
            return self.outer.get(name)
        else:
            return v

    def put_new(self, name, value):
        self.values[name] = value

    def put(self, name, value):
        e = self.where(name)

        if e == None:
            e = self

        e.put_new(name, value)

    def where(self, name):
        if self.values.get(name) != None:
            return self
        elif self.outer == None:
            return None
        else:
            return self.outer.where(name)

    def all(self):
        return {
            "values": self.values,
            "outer": self.outer
        }

    