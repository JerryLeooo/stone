from stone.ast.expr import *
from stone.common.exc import *

def category(original_cls):
    def _(cls):
        for k, v in filter(
            lambda item: not item[0].startswith("_"), cls.__dict__.items()
        ):
            setattr(original_cls, k, v)
    return _

class BasicEvaluator(object):

    @category(ASTTree)
    class ASTTreeEx(object):
        def eval(self, env):
            pass

    @category(ASTList)
    class ASTListEx(object): # eval ASTList
        def eval(self, env):
            raise StoneException("cannot eval: %s" % self.__str__, self)

    @category(ASTLeaf)
    class ASTLeafEx(object): # eval ASTLeaf
        def eval(self, env):
            raise StoneException("cannot eval: %s" % self.__str__, self)

    @category(NumberLiteral)
    class NumberEx(object):
        def eval(self, env):
            return self.value()

    @category(StringLiteral)
    class StringEx(object):
        def eval(self, env):
            return self.value()

    @category(Name)
    class NameEx(object):
        def eval(self, env):
            value = env.get(self.name())
            if value == None:
                raise StoneException("undefined name: %s" % self.name(), self)
            else:
                return value

    @category(NegativeExpr)
    class NegativeEx(object):
        def eval(self, env):
            v = self.operand().eval(env)
            if isinstance(v, int):
                return -v
            else:
                raise StoneException("bad type for -", self)

    @category(BinaryExpr)
    class BinaryEx(object):
        def eval(self, env):
            op = self.operator()
            if "=" == op:
                right = self.right().eval(env)
                return self.compute_assign(env, right)
            else:
                left = self.left().eval(env)
                right = self.right().eval(env)

                return self.compute_op(left, op, right)

        def compute_assign(self, env, rvalue):
            l = self.left()
            if isinstance(l, Name):
                env.put(l.name(), rvalue)
                return rvalue
            else:
                raise StoneException("bad assignment", self)

        def compute_op(self, left, op, right):
            if isinstance(left, int) and isinstance(right, int):
                return self.compute_number(left, op, right)
            else:
                if op == "+":
                    return left + right
                elif op == "==":
                    return left == right
                else:
                    raise StoneException("bad type", self)

        def compute_number(self, left, op, right):
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "*":
                return left * right
            elif op == "/":
                return left / right
            elif op == "%":
                return left % right
            elif op == "==":
                return left == right
            elif op == ">":
                return left > right
            elif op == "<":
                return left < right
            else:
                raise StoneException("bad operator", self)

    @category(BlockStmnt)
    class BlockEx(object):
        def eval(self, env):
            for t in self.children():
                if not isinstance(t, NullStmnt):
                    result = t.eval(env)
            return result

    @category(IfStmnt)
    class IfEx(object):
        def eval(self, env):
            c = self.condition().eval(env)
            if isinstance(c, int) and c != 0:
                return self.then_block().eval(env)
            else:
                b = self.else_block()
                if b is None:
                    return 0
                else:
                    return b.eval(env)

    @category(WhileStmnt)
    class WhileEx(object):
        def eval(self, env):
            result = 0
            while True:
                c = self.condition().eval(env)
                if isinstance(c, int) and c == 0:
                    return result
                else:
                    self.body().eval(env)
        