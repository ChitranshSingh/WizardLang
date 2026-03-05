"""Implementation of variable-creation spell handlers."""


def alohomora(line, env):
    """Create a variable from 'Alohomora name = value' syntax."""
    line = line.replace("Alohomora", "", 1).strip()
    name, value = line.split("=")

    name = name.strip()
    value = value.strip()

    if value.isdigit():
        value = int(value)
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    env.set_variable(name, value)
