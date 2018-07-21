import re
from queue import Queue
from stone.common.exc import ParseException
from stone.common.reader import LineNumberReader
from stone.lexer.token import Token, IdToken, NumberToken, StrToken

from stone.lexer.pattern import regex_pattern

class Lexer(object):
    def __init__(self, fp):
        self.reader = LineNumberReader(fp)
        self.queue = Queue()
        self.pattern = re.compile(regex_pattern)
        self.has_more = True
        self.line_no = 0

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

        pos, end_pos = 0, len(line) - 1

        while pos < end_pos:
            matcher = self.pattern.search(line[pos:end_pos])
            if matcher:
                self.add_token(line_no, matcher)
            else:
                raise ParseException(
                    "bad token at line %d: %s" % (line_no, line[pos: end_pos])
                )

            pos += matcher.end()

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
