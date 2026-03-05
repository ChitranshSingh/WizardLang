"""Implementation of the Legilimens spell (input)."""


def legilimens(line, env):
    """Prompt the user and store the input in a variable."""
    line = line.replace("Legilimens", "", 1).strip()
    value = input("🔮 Enter value: ")
    env.set_variable(line, value)
