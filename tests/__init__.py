import sys, os
print(sys.path)

def get_source_path(filename):
    pwd = os.path.abspath(os.path.join(__file__, os.pardir))
    return os.path.join(pwd, "sources", filename)