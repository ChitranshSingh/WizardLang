import sys
from wizardlang.core.interpreter import Interpreter

def main():
    if len(sys.argv) < 2:
        print("Usage: python wizard.py <file.wzl>")
        return

    filename = sys.argv[1]

    with open(filename, "r") as f:
        code = f.readlines()

    interpreter = Interpreter()
    interpreter.run(code)

if __name__ == "__main__":
    main()