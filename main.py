from interpreter import Environment, Interpreter
from lexer import Lexer
from parser import Parser
import sys


def execute_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()
        tokens = Lexer(code).tokenize()
        ast = Parser(tokens).parse()
        interpreter = Interpreter(ast)
        interpreter.interpret()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"Error executing file '{filename}': {e}")


def repl():
    print("Welcome to the Lambda Interpreter REPL. Type 'exit' to quit.")
    global_env = Environment()

    while True:
        try:
            code = input(">>> ")
            if code.lower() in {"exit", "quit"}:
                break

            tokens = Lexer(code).tokenize()
            ast = Parser(tokens).parse()
            interpreter = Interpreter(ast)
            result = interpreter.interpret()

            if result is not None:
                print(result)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1].endswith(".lambda"):
            execute_file(sys.argv[1])
        else:
            repl()
    except Exception as e:
        print(f"Unexpected error: {e}")
