regex_pattern = r'''
\s*(                                 # space
(//.*)|                              # comment
(\d+)                                # number
("[^"]*")|                           # string
[A-Z_a-z][A-z_a-z0-9]*|              # identifier
==|<=|>=|&&|\|\||                    # logic symbol
[\+\-\*/\{\}\=\|\&\[\]\(\)\<\>\;\%]  # opr symbol
'''