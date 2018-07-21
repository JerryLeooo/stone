from stone.lexer.lexer import Lexer
from stone.common.reader import LineNumberReader

def test_lexer():
    with open("hello.stone", "r") as fp:
        lexer = Lexer(LineNumberReader(fp))
        
        result = []
        t = lexer.read()
        while t:
            result.append(t)
            t = lexer.read()

        assert len(result) == 17

