import re
from queue import Queue
from stone.common.exc import ParseException
from stone.common.reader import LineNumberReader
from stone.lexer.token import Token, IdToken, NumberToken, StrToken

regex_pattern = (
r'\s*(' +
r'(//.*)|' + 
r'(\d+)|' + 
r'("[^"]*")|' + 
r'[A-Z_a-z][A-z_a-z0-9]*|' + 
r'==|<=|>=|&&|\|\||' + 
r'[\+\-\*/\{\}\=\|\&\[\]\(\)\<\>\;\%]' + 
r')')


class Lexer(object):
    def __init__(self, fp):
        self.reader = LineNumberReader(fp)
        self.queue = []
        self.pattern = re.compile(regex_pattern)
        self.has_more = True
        self.line_no = 0

    def read(self):
        if self.fill_queue(0):
            return self.queue.pop(0)
        return Token.EOF

    def peek(self, i):
        if self.fill_queue(i):
            return self.queue[i]
        return Token.EOF

    def add_token(self, line_no, matcher):
        m = matcher.group(1)
        if m is not None:  # not a space line
            if matcher.group(2) == None:  # not a comment
                if matcher.group(3) != None:
                    token = NumberToken(self.line_no, int(m))
                elif matcher.group(4) != None:
                    token = StrToken(self.line_no, m)
                else:
                    token = IdToken(self.line_no, m)
                self.queue.append(token)


    def fill_queue(self, i):
        while i >= len(self.queue):
            if self.has_more:
                self.read_line()
            else:
                return False

        return True

    def __str__(self):
        return "<Lexer: %s %s>" % (self.pattern, self.line_no)

    def read_line(self):
        line = ""

        try:
            line = self.reader.read_line()
        except IOError as e:
            raise ParseException(str(e))

        if not line:
            self.has_more = False
            return

        self.line_no = self.reader.get_line_number()

        pos, end_pos = 0, len(line) - 1

        while pos < end_pos:
            matcher = self.pattern.search(line[pos:end_pos])
            if matcher:
                self.add_token(self.line_no, matcher)
            else:
                raise ParseException(
                    "bad token at line %d: %s, where line is %s, and pos=%d, end_pos=%d" % (self.line_no, line[pos: end_pos], line, pos, end_pos)
                )

            pos += matcher.end()

        self.queue.append(IdToken(self.line_no, Token.EOL))
