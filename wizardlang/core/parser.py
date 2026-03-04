from wizardlang.core.spellbook import SPELLBOOK


def parse_line(line, env):

    parts = line.split()

    spell = parts[0]

    if line.startswith("Expecto") or line.startswith("Reparo"):
        return

    elif spell in SPELLBOOK:
        SPELLBOOK[spell](line, env)

    else:
        print(f"Unknown spell: {spell}")