class LineNumberReader(object):
    def __init__(self, fp):
        self.fp = fp
        self.current_line = 0
        self.lines = fp.readlines()
        self.total_lines = len(self.lines)

    def get_line_number(self):
        return self.current_line

    def read_line(self):
        if self.current_line < self.total_lines:
            line = self.lines[self.current_line]
            self.current_line += 1
            return line
        else:
            return None