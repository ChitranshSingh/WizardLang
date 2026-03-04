from wizardlang.core.spellbook import SPELLBOOK
from wizardlang.errors.error_handler import handle_error


def parse_line(line, env):

    parts = line.split()

    spell = parts[0]

    if line.startswith("Expecto") or line.startswith("Reparo"):
        return

    elif spell in SPELLBOOK:
        SPELLBOOK[spell](line, env)

    else:
        handle_error(env, f"Unknown spell '{spell}'")