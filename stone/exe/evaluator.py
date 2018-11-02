from stone.ast.expr import *
from stone.ast.func import *
from stone.common.exc import *

def category(original_cls):
    def _(cls):
        for k, v in filter(
            lambda item: not item[0].startswith("_") and not item[0] in original_cls.__dict__.items(), cls.__dict__.items()
        ):
            setattr(original_cls, k, v)
    return _

class BasicEvaluator(object):

    @category(ASTTree)
    class ASTTreeEx(ASTTree):
        def eval(self, env):
            pass

    @category(ASTList)
    class ASTListEx(ASTList): # eval ASTList
        def eval(self, env):
            raise StoneException("cannot eval: %s" % self.__str__, self)

    @category(ASTLeaf)
    class ASTLeafEx(ASTLeaf): # eval ASTLeaf
        def eval(self, env):
            raise StoneException("cannot eval: %s" % self.__str__, self)

    @category(NumberLiteral)
    class NumberEx(NumberLiteral):
        def eval(self, env):
            return self.value()

    @category(StringLiteral)
    class StringEx(StringLiteral):
        def eval(self, env):
            return self.value()

    @category(Name)
    class NameEx(Name):
        def eval(self, env):
            value = env.get(self.name())
            if value == None:
                raise StoneException("undefined name: %s" % self.name(), self)
            else:
                return value

    @category(NegativeExpr)
    class NegativeEx(NegativeExpr):
        def eval(self, env):
            v = self.operand().eval(env)
            if isinstance(v, int):
                return -v
            else:
                raise StoneException("bad type for -", self)

    @category(BinaryExpr)
    class BinaryEx(BinaryExpr):
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
            print(left, op, right)
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
    class BlockEx(BlockStmnt):
        def eval(self, env):
            for t in self.children():
                if not isinstance(t, NullStmnt):
                    result = t.eval(env)
            return result

    @category(IfStmnt)
    class IfEx(IfStmnt):
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
    class WhileEx(WhileStmnt):
        def eval(self, env):
            result = 0
            while True:
                c = self.condition().eval(env)
                if isinstance(c, int) and c == 0:
                    return result
                else:
                    self.body().eval(env)

class FuncEvaluator(object):
    @category(DefStmnt)
    class DefStmntEx(DefStmnt):
        def eval(self, env):
            env.put_new(self.name(), Function(self.parameters(), self.body(), env))
            return self.name()

    @category(PrimaryExpr)
    class PrimaryEx(PrimaryExpr):
        def operand(self):
            return self.child(0)

        def postfix(self, nest):
            return self.child(self.num_children() - nest - 1)

        def has_postfix(self, nest):
            return self.num_children() - nest > 1

        def eval(self, env):
            return self.eval_sub_expr(env, 0)

        def eval_sub_expr(self, env, nest):
            if self.has_postfix(nest):
                target = self.eval_sub_expr(env, nest + 1)
                return self.postfix(nest).eval(env, target)
            else:
                return self.operand().eval(env)

    @category(Argument)
    class ArgumentEx(Argument):
        def eval(self, caller_env, value):
            if not isinstance(value, Function):
                raise StoneException("bad function", self)

            func = value
            params = func.parameters()
            if self.size() != params.size():
                raise StoneException("bad number of arguments", self)

            new_env = func.make_env()
            num = 0
            for a in self.children():
                params.eval(new_env, num, a.eval(caller_env))
                num += 1

            return func.body().eval(new_env)

    @category(ParameterList)
    class ParamsEx(ParameterList):
        def eval(self, env, index, value):
            env.put_new(self.name(index), value)

class ClosureEvaluator(object):
    @category(Fun)
    class FunEx(Fun):
        def eval(self, env):
            return Function(self.parameters(), self.body(), env) 
    