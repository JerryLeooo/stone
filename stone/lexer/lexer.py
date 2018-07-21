import re
from queue import Queue
from stone.common.exc import ParseException
from stone.common.reader import LineNumberReader
from stone.lexer.token import Token, IdToken

class Lexer(object):

    regex_pattern = r'''
    \s*(                                 # space
    (//.*)|                              # comment
    (\d+)                                # number
    ("[^"]*")|                           # string
    [A-Z_a-z][A-z_a-z0-9]*|              # identifier
    ==|<=|>=|&&|\|\||                    # logic symbol
    [\+\-\*/\{\}\=\|\&\[\]\(\)\<\>\;\%]  # opr symbol
    '''

    def __init__(self, reader):
        self.has_more = True
        self.reader = LineNumberReader(reader)
        self.queue = Queue()
        self.line_no = 0
        self.pattern = re.compile(self.regex_pattern)

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
            raise ParseException(e.message, e.errors)

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
