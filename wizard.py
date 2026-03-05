"""CLI entrypoint for running WizardLang scripts from the terminal."""

import sys

from wizardlang.core.interpreter import Interpreter


def main():
    """Load a .wzl file and execute it with the interpreter."""
    if len(sys.argv) < 2:
        print("Usage: python wizard.py <file.wzl>")
        return

    filename = sys.argv[1]

    with open(filename, "r", encoding="utf-8") as source_file:
        code = source_file.readlines()

    interpreter = Interpreter()
    interpreter.run(code)


if __name__ == "__main__":
    main()
