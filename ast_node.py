
class ASTNode:
    pass


class FunctionDefinition(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"FunctionDefinition(name={self.name}, params={self.params}, body={self.body})"


class LambdaExpression(ASTNode):
    def __init__(self, params, body):
        self.params = params  # List of parameters
        self.body = body

    def __repr__(self):
        return f"LambdaExpression(params={self.params}, body={self.body})"


class FunctionApplication(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __repr__(self):
        return f"FunctionApplication(func={self.func}, args={self.args})"


class IfStatement(ASTNode):
    def __init__(self, condition, consequence, alternative=None):
        self.condition = condition      # The condition to evaluate
        self.consequence = consequence  # The block to execute if the condition is true
        self.alternative = alternative  # The block to execute if the condition is false

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, consequence={self.consequence}, alternative={self.alternative})"


class BinaryOperation(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryOperation(left={self.left}, operator={self.operator}, right={self.right})"


class UnaryOperation(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"UnaryOperation(operator={self.operator}, operand={self.operand})"


class IntegerLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"IntegerLiteral(value={self.value})"


class BooleanLiteral(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral(value={self.value})"


class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier(name={self.name})"
