from wizardlang.spells.lumos import lumos
from wizardlang.spells.variables import alohomora
from wizardlang.spells.input_spell import legilimens
from wizardlang.spells.math_spells import leviosa, descendo


def parse_line(line, env):

    if line.startswith("Expecto"):
        return
    
    elif line.startswith("Lumos"):
        lumos(line, env)

    elif line.startswith("Alohomora"):
        alohomora(line, env)

    elif line.startswith("Legilimens"):
        legilimens(line, env)

    elif line.startswith("Leviosa"):
        leviosa(line, env)

    elif line.startswith("Descendo"):
        descendo(line, env)

    elif line.startswith("AvadaKedavra"):
        exit()

    else:
        print("Unknown spell:", line)