import re


class Lexer:
    def __init__(self, code):
        self.code = code
        self.line_num = 1
        self.line_start = 0
        self.tokens = []

    token_specification = [
        ('DEFUN', r'\bDefun\b'),  # Function definition keyword
        ('NAME', r'\bname\b'),  # Function name reserved word
        ('ARGUMENTS', r'\barguments\b'),  # Function arguments reserved word
        ('LAMBD', r'\bLambd\b'),  # Lambda keyword
        ('IF', r'\bif\b'),  # If keyword
        ('ELSE', r'\belse\b'),  # Else keyword
        ('INTEGER', r'-?\d+'),  # Integer (including negative integers)
        ('BOOL', r'\bTrue\b|\bFalse\b'), # Boolean
        ('ID', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),  # Identifiers
        ('ARITH_OP', r'[-+*/%]'),  # Arithmetic Operators
        ('BOOL_OP', r'&&|\|\|'),  # Boolean Operators
        ('COMP_OP', r'==|!=|>=|<=|>|<'),  # Comparison Operators
        ('NOT', r'!'),                # Not Operators
        ('LPAREN', r'\('),            # Left parenthesis
        ('RPAREN', r'\)'),            # Right parenthesis
        ('LBRACE', r'\{'),            # Left brace
        ('RBRACE', r'\}'),            # Right brace
        ('COMMA', r','),              # Comma
        ('COLON', r':'),              # Colon
        ('DOT', r'\.'),               # Dot
        ('NEWLINE', r'\n'),           # Line endings
        ('SKIP', r'[ \t]+'),          # Skip over spaces and tabs
        ('COMMENT', r'#.*'),         # Single line comment
        ('MISMATCH', r'.'),           # Any other character
    ]

    # The master regular expression
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    def tokenize(self):
        for mo in re.finditer(self.tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group(kind)
            column = mo.start() - self.line_start
            if kind == 'INTEGER':
                value = int(value)
            elif kind == 'BOOL':
                value = True if value == 'True' else False
            elif kind == 'NEWLINE':
                self.line_start = mo.end()
                self.line_num += 1
                continue
            elif kind == 'SKIP' or kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected on line {self.line_num}')
            self.tokens.append((kind, value, self.line_num, column))
        self.tokens.append(('EOF', 'EOF', self.line_num, column))
        return self.tokens


