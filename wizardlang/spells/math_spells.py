def leviosa(line, env):

    name = line.replace("Leviosa", "", 1).strip()

    value = env.get_variable(name)

    env.set_variable(name, value + 1)


def descendo(line, env):

    name = line.replace("Descendo", "", 1).strip()

    value = env.get_variable(name)

    env.set_variable(name, value - 1)