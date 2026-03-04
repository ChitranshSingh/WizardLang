from wizardlang.spells.lumos import lumos
from wizardlang.spells.variables import alohomora
from wizardlang.spells.input_spell import legilimens
from wizardlang.spells.math_spells import leviosa, descendo
from wizardlang.spells.hogwarts import hogwarts


def parse_line(line, env):

    if line.startswith("Expecto") or line.startswith("Reparo"):
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
    
    elif line.startswith("Hogwarts"):
        hogwarts(line, env)

    else:
        print("Unknown spell:", line)