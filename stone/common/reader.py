class LineNumberReader(object):
    def __init__(self, fp):
        self.fp = fp
        self.current_line = 0
        self.lines = fp.readlines()

    def get_line_number(self):
        return self.current_line

    def read_line(self):
        line = self.lines[self.current_line]
        self.current_line += 1
        return line