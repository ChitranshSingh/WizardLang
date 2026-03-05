"""Parses and dispatches single WizardLang lines to spell handlers."""

from wizardlang.core.spellbook import SPELLBOOK
from wizardlang.errors.error_handler import handle_error


def parse_line(line, env):
    """Execute one spell line using the global SPELLBOOK registry."""
    parts = line.split()
    if not parts:
        return

    spell = parts[0]

    # These two are block-control spells handled at interpreter level.
    if line.startswith("Expecto") or line.startswith("Reparo"):
        return

    if spell in SPELLBOOK:
        SPELLBOOK[spell](line, env)
        return

    handle_error(env, f"Unknown spell '{spell}'")
