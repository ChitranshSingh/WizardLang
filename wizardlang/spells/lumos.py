"""Implementation of the Lumos spell (output)."""


def lumos(line, env):
    """Print a string literal or the value of a variable."""
    text = line.replace("Lumos", "", 1).strip()

    if text.startswith('"') and text.endswith('"'):
        print(text[1:-1])
        return

    print(env.get_variable(text))
