from ast_node import FunctionDefinition, LambdaExpression, FunctionApplication, Identifier, \
    IntegerLiteral, BooleanLiteral, UnaryOperation, BinaryOperation, IfStatement


class BNFLoader:
    def __init__(self, bnf_file_path):
        self.rules = self.load_bnf(bnf_file_path)

    def load_bnf(self, file_path):
        rules = {}
        with open(file_path, 'r') as file:
            content = file.read()
            lines = content.splitlines()
            current_non_terminal = None
            for line in lines:
                if line.strip() == "":
                    continue
                if "::=" in line:
                    parts = line.split("::=")
                    current_non_terminal = parts[0].strip()
                    rules[current_non_terminal] = [p.strip() for p in parts[1].split("|")]
                else:
                    rules[current_non_terminal].extend([p.strip() for p in line.split("|")])
        return rules


class Parser:
    def __init__(self, tokens, bnf_file_path=None, debug=False):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if tokens else None
        self.debug = debug
        self.rules = BNFLoader(bnf_file_path).rules if bnf_file_path else None

    def log(self, message):
        if self.debug:
            print(message)

    def error(self, message):
        line = self.current_token[2]
        col = self.current_token[3]
        raise SyntaxError(
            f"Syntax Error at line {line}, column {col}: {message}. Current token: {self.current_token[0]}")

    def advance(self):
        self.log(f"Advancing from {self.current_token}")
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = ('EOF', 'EOF', -1, -1)
        self.log(f"Current token is now {self.current_token}")

    def expect(self, token_type):
        self.log(f"Expecting {token_type}, current token: {self.current_token[0]}")
        if self.current_token and self.current_token[0] == token_type:
            self.advance()
        else:
            self.error(f"Expected token {token_type} but got {self.current_token[0]}")

    def parse(self):
        try:
            self.log("Starting parsing...")
            result = self.program()
            self.log("Finished parsing.")
            return result
        except Exception as e:
            raise RuntimeError(f"Parsing failed: {str(e)}")

    def program(self):
        self.log("Parsing program...")
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
        self.log(f"Program parsed with {len(statements)} statement(s).")
        return statements

    def parse_statement(self):
        self.log(f"Parsing statement with token: {self.current_token}")
        if self.current_token[0] == 'DEFUN':
            return self.parse_function_def()
        elif self.current_token[0] == 'IF':
            return self.parse_if_statement()
        elif self.current_token[0] == 'LPAREN' and self.tokens[self.pos + 1][0] == 'LAMBD':
            return self.parse_lambda_expr()
        else:
            return self.parse_expression()

    def parse_function_def(self):
        self.log("Parsing function definition")
        try:
            self.expect('DEFUN')
            self.expect('LBRACE')
            self.expect('NAME')
            self.expect('COLON')
            func_name = self.current_token[1]
            self.expect('ID')
            self.expect('COMMA')
            self.expect('ARGUMENTS')
            self.expect('COLON')
            params = self.parse_params()
            self.expect('RBRACE')
            if self.current_token[0] == 'IF':
                body = self.parse_if_statement()
            else:
                body = self.parse_expression()
            self.log(f"Function def '{func_name}' with params: {params}, and body: {body}")
            return FunctionDefinition(name=func_name, params=params, body=body)
        except SyntaxError as e:
            self.error(f"Error parsing function definition: {e}")

    def parse_if_statement(self):
        try:
            self.log("Parsing if statement")
            self.expect('IF')
            condition = self.parse_expression()
            self.expect('LBRACE')
            consequence = self.parse_expression()
            self.expect('RBRACE')
            alternative = None
            if self.current_token[0] == 'ELSE':
                self.expect('ELSE')
                self.expect('LBRACE')
                alternative = self.parse_expression()
                self.expect('RBRACE')
            return IfStatement(condition, consequence, alternative)
        except SyntaxError as e:
            self.error(f"Error parsing if statement: {e}")

    def parse_lambda_expr(self):
        self.log("Parsing lambda expression")
        self.expect('LPAREN')
        self.expect('LAMBD')
        if self.current_token[0] == 'ID':
            params = self.current_token[1]
            self.expect('ID')
            self.expect('DOT')
        body = self.parse_expression()
        self.expect('RPAREN')
        lambda_expr = LambdaExpression(params=params, body=body)
        self.log(f"Constructed lambda expression: {lambda_expr}")
        if self.current_token[0] == 'LPAREN':
            self.log("Lambda expression is followed by a call, parsing lambda call")
            return self.parse_lambda_call(lambda_expr)
        return lambda_expr

    def parse_lambda_call(self, func):
        self.log(f"Parsing lambda call for: {func}")
        self.expect('LPAREN')
        args = self.parse_args()
        self.expect('RPAREN')
        self.log(f"lambda call '{func}' with args: {args}")
        return FunctionApplication(func=func, args=args)

    def parse_function_call(self, func):
        self.log(f"Parsing function call for: {func}")
        func = self.current_token[1]
        self.expect('ID')
        self.expect('LPAREN')
        args = self.parse_args()
        self.expect('RPAREN')
        self.log(f"Function call '{func}' with args: {args}")
        return FunctionApplication(func=func, args=args)

    def parse_params(self):
        self.log("Parsing parameters")
        params = []
        self.expect('LPAREN')
        while self.current_token[0] == 'ID' and self.tokens[self.pos + 1][0] == 'COMMA':
            params.append(self.current_token[1])
            self.expect('ID')
            self.expect('COMMA')
        self.expect('RPAREN')
        return params

    def parse_args(self):
        self.log("Parsing arguments")
        args = []
        while self.current_token[0] != 'RPAREN':
            args.append(self.parse_expression())
            if self.current_token[0] == 'COMMA':
                self.expect('COMMA')
            elif self.current_token[0] == 'RPAREN':
                break
            else:
                self.error(f"Unexpected token in argument list: {self.current_token}")
        return args

    def parse_expression(self):
        self.log(f"Parsing expression with token: {self.current_token}")

        def parse_term():
            if self.current_token[0] == 'NOT':
                op = self.current_token[1]
                self.expect('NOT')
                expr = self.parse_expression()
                unary_op = UnaryOperation(op, expr)
                return unary_op

            if self.current_token[0] == 'ID' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'LPAREN':
                return self.parse_function_call(self.current_token[1])

            if self.current_token[0] == 'LPAREN' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][0] == 'LAMBD':
                return self.parse_lambda_expr()

            if self.current_token[0] == 'INTEGER':
                number = IntegerLiteral(self.current_token[1])
                self.expect('INTEGER')
                return number

            if self.current_token[0] == 'BOOL':
                boolean = BooleanLiteral(self.current_token[1])
                self.expect('BOOL')
                return boolean

            if self.current_token[0] == 'ID':
                identifier = Identifier(self.current_token[1])
                self.expect('ID')
                return identifier

            if self.current_token[0] == 'LPAREN':
                self.expect('LPAREN')
                expr = self.parse_expression()
                self.expect('RPAREN')
                return expr

            self.error(
                f"Unexpected token: '{self.current_token[0]}' at line {self.current_token[2]}, column {self.current_token[3]}")

        def parse_operation(parse_func, valid_operators):
            left = parse_func()
            while self.current_token[0] in valid_operators:
                op = self.current_token[1]
                self.expect(self.current_token[0])
                right = parse_func()
                left = BinaryOperation(left, op, right)
            return left

        return parse_operation(parse_term, {'ARITH_OP', 'BOOL_OP', 'COMP_OP'})