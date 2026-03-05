"""Implementation of simple arithmetic WizardLang spells."""


def leviosa(line, env):
    """Increment a numeric variable by 1."""
    name = line.replace("Leviosa", "", 1).strip()
    value = env.get_variable(name)
    env.set_variable(name, value + 1)


def descendo(line, env):
    """Decrement a numeric variable by 1."""
    name = line.replace("Descendo", "", 1).strip()
    value = env.get_variable(name)
    env.set_variable(name, value - 1)
