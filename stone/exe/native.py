from stone.ast.func import NativeFunction
from stone.common.exc import StoneException
import time

class Natives(object):
    def environment(self, env):
        self.append_natives(env)
        return env

    def append_natives(self, env):
        self.append(env, "println", self.__class__, "println", object)
        self.append(env, "read", self.__class__, "read")
        self.append(env, "length", self.__class__, "length", object)
        self.append(env, "to_int", self.__class__, "to_int", object)
        self.append(env, "current_time", self.__class__, "current_time")

    def append(self, env, name, clazz, method_name, params=None):
        try:
            m = getattr(clazz, method_name)
        except Exception as e:
            print(e)
            raise StoneException("cannot find a native function: %s.%s" % (clazz, method_name), self)
        
        env.put(name, NativeFunction(method_name, m))

    def println(self, obj):
        print(obj)
        return 0

    def read(self):
        pass

    def length(self, s):
        return len(s)

    def to_int(self, value):
        if isinstance(value, str):
            return int(value)
        elif isinstance(value, int):
            return value
        else:
            raise StoneException("cannot convert to number", str(value))

    def current_time(self):
        return int(time.time())



    