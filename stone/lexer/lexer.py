import re
from queue import Queue
from stone.common.exc import ParseException
from stone.common.reader import LineNumberReader
from stone.lexer.token import Token, IdToken, NumberToken, StrToken

from stone.lexer.pattern import regex_pattern

class Lexer(object):
    def __init__(self, reader):
        self.has_more = True
        self.reader = LineNumberReader(reader)
        self.queue = Queue()
        self.line_no = 0
        self.pattern = re.compile(regex_pattern)

    def read(self):
        if self.fill_queue(0):
            return self.queue.get()
        else:
            return Token.EOF

    def fill_queue(self, i):
        while i >= self.queue.qsize():
            if self.has_more:
                self.read_line()
            else:
                return False

        return True

    def read_line(self):
        line = ""

        try:
            line = self.reader.read_line()
        except IOError as e:
            raise ParseException(str(e))

        if not line:
            self.has_more = False
            return

        line_no = self.reader.get_line_number()

        pos, end_pos = 0, len(line)

        while pos < end_pos:
            matcher = self.pattern.search(line[pos:end_pos])
            pos += matcher.end()
            if matcher:
                self.add_token(line_no, matcher)
            else:
                raise ParseException("bad token at line " + line_no)

            self.queue.put(IdToken(line_no, Token.EOL))

    def add_token(self, line_no, matcher):
        m = matcher.group(0)
        if m:
            if not matcher.group(2):
                token = None
                if matcher.group(3):
                    token = NumberToken(line_no, int(m))
                elif matcher.group(4):
                    token = StrToken(line_no, m)
                else:
                    token = IdToken(line_no, m)

                self.queue.put(token)
