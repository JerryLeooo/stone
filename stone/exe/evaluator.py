from stone.ast.expr import *
from stone.common.exc import *

class BasicEvaluator(object):
    class ASTTreeEx(ASTTree):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            pass

    class ASTListEx(ASTList): # eval ASTList
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            raise StoneException("cannot eval: %s" % self.__str__, self)

    class ASTLeafEx(ASTLeaf): # eval ASTLeaf
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            raise StoneException("cannot eval: %s" % self.__str__, self)

    class NumberEx(NUmberLiteral):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            return self.elem.value()

    class StringEx(StringLiteral):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            return self.value()

    class NameEx(Name):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            value = env.get(self.name())
            if value == None:
                raise StoneException("undefined name: %s" % self.name(), self)
            else:
                return value

    class NegativeEx(NegativeExpr):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            v = self.operand().eval(env)
            if isinstance(v, int):
                return -v
            else:
                raise StoneException("bad type for -", self)

    class BinaryEx(BinaryExpr):
        def eval(self, env):
            op = self.operator()
            if "=" == op:
                right = self.left().eval(env)
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

    class BlockEx(BlockStmnt):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            for t in self:
                if not isinstance(t, NullStmnt):
                    result = t.eval(env)
            return result

    class IfEx(IfStmnt):
        def __init__(self, elem):
            self.elem = elem

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

    class WhileEx(WhileStmnt):
        def __init__(self, elem):
            self.elem = elem

        def eval(self, env):
            result = 0
            while True:
                c = self.condition().eval(env)
                if isinstance(c, int) and c == 0:
                    return result
                else:
                    self.body().eval(env)
        