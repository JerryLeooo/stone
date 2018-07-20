class Lexer(object):
    def __init__(self, reader):
        self._has_more = True
        self._reader = LineNumberReader(reader)
