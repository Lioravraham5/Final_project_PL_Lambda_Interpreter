from ast_node import FunctionDefinition, LambdaExpression, FunctionApplication, Identifier, \
    IntegerLiteral, BooleanLiteral, UnaryOperation, BinaryOperation, IfStatement


class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.env = {}

    def get(self, name):
        if name in self.env:
            return self.env[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise NameError(f"Undefined variable: {name}")

    def set(self, name, value):
        self.env[name] = value

    def extend(self, names, values):
        child = Environment(self)
        for name, value in zip(names, values):
            child.set(name, value)
        return child


class Interpreter:
    def __init__(self, ast):
        self.ast = ast
        self.global_env = Environment()

    def interpret(self):
        print("Starting interpretation...")
        try:
            result = None
            for node in self.ast:
                try:
                    result = self.eval(node, self.global_env)
                    if result is not None:
                        print(result)
                except Exception as e:
                    print(f"Error during interpretation of node {node}: {e}")
            print("Interpretation finished...")
            return result
        except Exception as e:
            raise RuntimeError(f"Runtime error during interpretation: {str(e)}")

    def eval(self, node, env):
        if isinstance(node, IntegerLiteral):
            return node.value

        elif isinstance(node, BooleanLiteral):
            return node.value

        elif isinstance(node, Identifier):
            return env.get(node.name)

        elif isinstance(node, BinaryOperation):
            left = self.eval(node.left, env)
            # For logical OR (||), short-circuit if left side is True
            if node.operator == '||' and left:
                return True
            # For logical AND (&&), short-circuit if left side is False
            if node.operator == '&&' and not left:
                return False
            right = self.eval(node.right, env)
            return self.apply_operator(node.operator, left, right)

        elif isinstance(node, UnaryOperation):
            value = self.eval(node.operand, env)
            return self.apply_unary_operator(node.operator, value)

        elif isinstance(node, FunctionDefinition):
            env.set(node.name, (node.params, node.body, env))
            return None

        elif isinstance(node, LambdaExpression):
            return node.params, node.body, env

        elif isinstance(node, FunctionApplication):
            try:
                # Check if the function is a string (indicating it's an identifier for a named function)
                if isinstance(node.func, str):
                    func = env.get(node.func)
                else:
                    func = self.eval(node.func, env)

                # Evaluate the arguments
                args = [self.eval(arg, env) for arg in node.args]

                # If the function is a regular function or lambda, apply the arguments
                if isinstance(func, tuple) and len(func) == 3:
                    params, body, closure_env = func

                    if isinstance(params, list):  # Regular function call
                        if len(params) != len(args):
                            raise TypeError(f"Function expected {len(params)} arguments but got {len(args)}")

                        new_env = closure_env.extend(params, args)
                        return self.eval(body, new_env)
                    else:  # Lambda expression
                        for arg in args:
                            func = self.apply_function(func, [arg])
                        return func

                else:
                    raise TypeError(f"Expected a function or lambda expression, but got: {func}")

            except Exception as e:
                raise RuntimeError(f"Error applying function: {str(e)}")

        elif isinstance(node, IfStatement):
            try:
                condition_value = self.eval(node.condition, env)
                if condition_value:
                    return self.eval(node.consequence, env)
                elif node.alternative is not None:
                    return self.eval(node.alternative, env)
                return None
            except Exception as e:
                raise RuntimeError(f"Error evaluating if-statement: {str(e)}")

        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def apply_function(self, func, args):
        param, body, closure_env = func

        if len(args) != 1:
            raise TypeError("Each lambda expression should receive exactly one argument.")

        new_env = closure_env.extend([param], args)
        result = self.eval(body, new_env)
        return result

    def apply_operator(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero is not allowed")
            return left // right
        elif op == '%':
            return left % right
        elif op == '&&':
            return left and right
        elif op == '||':
            return left or right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '>':
            return left > right
        elif op == '<':
            return left < right
        elif op == '>=':
            return left >= right
        elif op == '<=':
            return left <= right
        else:
            raise TypeError(f"Unknown operator: {op}")

    def apply_unary_operator(self, op, value):
        if op == '!':
            return not value
        else:
            raise TypeError(f"Unknown unary operator: {op}")