def legilimens(line, env):

    line = line.replace("Legilimens", "", 1).strip()

    value = input("🔮 Enter value: ")

    env.set_variable(line, value)