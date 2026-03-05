# WizardLang

WizardLang is a fun beginner-first programming language inspired by Harry Potter spells.
You write magical commands like `Lumos` and `Alohomora`, and the interpreter runs them as real program logic.

This repository also includes a Hogwarts-themed IDE built with PyQt6.

## Features

### Language
- Spell-based syntax for output, variables, input, loops, conditionals, and math updates
- House-aware error messages (`Gryffindor`, `Ravenclaw`, `Hufflepuff`, `Slytherin`)
- Simple Python interpreter core for easy learning

### IDE
- Syntax highlighting for spells
- Autocomplete popup while typing
- Line numbers in the editor
- Spellbook side panel with click-to-insert templates
- Spell documentation tooltips in spellbook
- Spell documentation popup on editor hover
- Resizable split layout:
  - horizontal splitter: Spellbook and Editor
  - vertical splitter: Editor area and Output area
- Run mode and Debug mode
- Open/Save `.wzl` files
- Hogwarts theme selector
- Startup splash screen

## Installation

1. Clone the repository.

```bash
git clone https://github.com/yourusername/wizardlang.git
cd wizardlang
```

2. Create and activate a virtual environment.

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies.

```bash
pip install PyQt6
```

## Running WizardLang

Run a script file:

```bash
python wizard.py examples/hello.wzl
```

Run the IDE:

```bash
python wizardlang/ide/wizard_ide.py
```

## Get Started with WizardLang

New here and just exploring for fun? Start with this path.

### 1. Learn 5 core spells
- `Lumos "text"`: print text
- `Alohomora x = 1`: create variable
- `Leviosa x`: increment variable
- `Descendo x`: decrement variable
- `Legilimens name`: take input

### 2. Learn flow spells
- `Expecto condition` ... `Otherwise` ... `EndSpell`
- `Reparo counter until 5` ... `EndSpell`

### 3. First script

```wzl
Hogwarts Gryffindor
Lumos "Welcome to WizardLang!"

Alohomora counter = 1
Reparo counter until 4
    Lumos counter
    Leviosa counter
EndSpell
```

### 4. Try in IDE
- Open the IDE
- Click spells from the Spellbook
- Hover a spell in the editor to read quick docs
- Click `🔍 Debug Spell` to see line-by-line execution

## Spell Reference

| Spell | Purpose |
| --- | --- |
| `Lumos` | Print output to console |
| `Alohomora` | Create variable |
| `Legilimens` | Read input |
| `Reparo` | Loop until a limit |
| `Expecto` | Conditional start |
| `Otherwise` | Else branch |
| `EndSpell` | Close loop/condition block |
| `Leviosa` | Increment variable |
| `Descendo` | Decrement variable |
| `Hogwarts` | Select house mode |

## Debug Mode

In IDE, click `🔍 Debug Spell` to get traces like:

```text
🔍 Debugging Spell Execution
Line 2 -> Variable 'counter' set to 1
Line 3 -> Reparo loop on 'counter' until 4
Line 3 -> Reparo iteration 1 (counter=1)
Line 4 -> Lumos executed
Line 5 -> Variable 'counter' incremented to 2
```

This helps beginners understand what each line does during runtime.

## Project Structure

```text
wizardlang/
  core/          # interpreter, parser, environment, spell registry
  spells/        # spell handler implementations
  houses/        # house-specific error styles
  errors/        # runtime error routing
  ide/           # PyQt6 IDE
wizard.py        # CLI runner
examples/        # sample .wzl programs
```

## Contributing

Contributions are welcome:
- new spells
- IDE improvements
- tests and docs
- beginner tutorials/examples

## License

MIT
