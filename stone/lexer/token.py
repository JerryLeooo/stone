from stone.common.exc import StoneException

class Token(object):

    def __init__(self, line):
        self._line_number = line

    def get_line_number(self):
        return self._line_number

    def is_identifier(self):
        return False

    def is_number(self):
        return False

    def is_string(self):
        return False

    def get_number(self):
        raise StoneException("Not number token")

    def next(self):
        return ""
    
    def text(self):
        return self.__class__
    
Token.EOF = Token(-1)
Token.EOL = "\n"

class IdToken(Token):

    def __init__(self, line_no, id):
        super().__init__(line_no)
        self._text = id

    def is_identifier(self):
        return True

    def text(self):
        return self._text

class NumberToken(Token):

    def __init__(self, line_no, v):
        super().__init__(line_no)
        self.value = v

    def is_number(self):
        return True

    def text(self):
        return str(self.value)

    def get_number(self):
        return self.value

class StrToken(Token):

    def __init__(self, line_no, string):
        super().__init__(line_no)
        self.literal = string

    def is_string(self):
        return True

    def text(self):
        return self.literal