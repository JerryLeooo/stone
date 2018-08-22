class LineNumberReader(object):
    def __init__(self, fp):
        self.fp = fp
        self.line_no = 0

    def get_line_number(self):
        return self.line_no

    def read_line(self):
        self.line_no = self.line_no + 1
        return self.fp.readline()