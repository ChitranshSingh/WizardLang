"""Central registry that maps WizardLang spell names to Python handlers."""

from wizardlang.spells.hogwarts import hogwarts
from wizardlang.spells.input_spell import legilimens
from wizardlang.spells.lumos import lumos
from wizardlang.spells.math_spells import descendo, leviosa
from wizardlang.spells.variables import alohomora


SPELLBOOK = {
    "Lumos": lumos,
    "Alohomora": alohomora,
    "Legilimens": legilimens,
    "Leviosa": leviosa,
    "Descendo": descendo,
    "Hogwarts": hogwarts,
}
