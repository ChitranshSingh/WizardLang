def lumos(line, env):

    text = line.replace("Lumos", "", 1).strip()

    if text.startswith('"') and text.endswith('"'):
        print(text[1:-1])

    else:
        print(env.get_variable(text))