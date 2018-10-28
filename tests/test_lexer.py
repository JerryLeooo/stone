import os
from stone.lexer.lexer import Lexer
from stone.lexer.token import Token
from . import get_source_path

def test_lexer_simple_read():
    with open(get_source_path("simple.stone"), "r") as fp:
        lexer = Lexer(fp)

        t = lexer.read()
        assert t.get_text() == "sum"

def test_lexer_read():
    with open(get_source_path("hello.stone"), "r") as fp:
        lexer = Lexer(fp)

        t = lexer.read()
        assert t.get_text() == "sum"

        t = lexer.read()
        assert t.get_text() == "=" # not right now, should do trim

def test_lexer():
    with open(get_source_path("hello.stone"), "r") as fp:
        lexer = Lexer(fp)

        result = []
        t = lexer.read()

        assert t.get_text() == "sum"

        while t != Token.EOF:
            result.append(t)
            t = lexer.read()

        assert len(result) == 30

def test_eol():
    assert Token.EOL == "\n"