# 🧙 WizardLang

### The Harry Potter Inspired Programming Language

WizardLang is a **fun, beginner-friendly programming language inspired by the Wizarding World of Harry Potter**.
Instead of writing traditional programming syntax, you **cast spells** to perform operations.

WizardLang is designed to make programming **magical, intuitive, and enjoyable**, even for beginners or young learners.

This project also includes a **custom Hogwarts-themed IDE** with features like syntax highlighting, spell autocomplete, house themes, and more.

---

# ✨ Features

### 🪄 WizardLang Language

* Magical syntax based on **Harry Potter spells**
* Beginner-friendly commands
* Simple interpreter written in Python
* Variables, loops, and conditionals
* House-based runtime personality system

### 🏰 Hogwarts IDE

* Custom **WizardLang IDE built using PyQt**
* Syntax highlighting for spells
* Spell autocomplete
* Line numbers in editor
* House-based color themes
* Open / Save `.wzl` programs
* Magical startup splash screen
* Integrated code execution

---

# 📸 Screenshots

*(Add screenshots after uploading the project)*

Example:

```
docs/screenshots/editor.png
docs/screenshots/splash.png
```

---

# 🧠 Why WizardLang?

Programming languages can feel intimidating to beginners.

WizardLang solves this by replacing traditional syntax with **intuitive magical commands**.

Example comparison:

Python:

```
print("Hello World")
```

WizardLang:

```
Lumos "Hello World"
```

Programming becomes **casting spells**.

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/wizardlang.git
cd wizardlang
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate it:

Windows:

```
venv\Scripts\activate
```

Linux / Mac:

```
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```
pip install PyQt6
```

---

# ▶ Running WizardLang Programs

Run a `.wzl` file:

```
python wizard.py examples/hello.wzl
```

---

# 🏰 Running the IDE

Launch the WizardLang IDE:

```
python wizardlang/ide/wizard_ide.py
```

---

# 📜 WizardLang Language Guide

WizardLang programs are written in files with extension:

```
.wzl
```

Example file:

```
hello.wzl
```

---

# 🪄 Basic Syntax

WizardLang uses **spells as commands**.

Example:

```
Lumos "Hello Wizard"
```

Output:

```
Hello Wizard
```

---

# 🧙 House System

Programs can select a Hogwarts house:

```
Hogwarts Gryffindor
```

Available houses:

```
Gryffindor
Ravenclaw
Hufflepuff
Slytherin
```

House mode affects:

* error messages
* IDE theme
* runtime personality

---

# 📦 Variables

Variables are created using **Alohomora**.

```
Alohomora name = "Harry"
```

Use variable:

```
Lumos name
```

---

# 📥 Input

Read user input using **Legilimens**.

```
Legilimens name
```

---

# 🔁 Loops

WizardLang uses **Reparo** loops.

Example:

```
Alohomora counter = 1

Reparo counter until 5
    Lumos counter
    Leviosa counter
EndSpell
```

Equivalent Python:

```
while counter < 5:
```

---

# 🔀 Conditional Statements

WizardLang uses **Expecto**.

```
Expecto age >= 18
    Lumos "Adult wizard"
Otherwise
    Lumos "Hogwarts student"
EndSpell
```

---

# 🔼 Increment

Increase variable using **Leviosa**.

```
Leviosa counter
```

Equivalent:

```
counter += 1
```

---

# 🔽 Decrement

Decrease variable using **Descendo**.

```
Descendo counter
```

Equivalent:

```
counter -= 1
```

---

# 📤 Output

Print text using **Lumos**.

```
Lumos "Hello Wizard"
```

---

# 🧾 Spell Reference

| Spell      | Purpose            |
| ---------- | ------------------ |
| Lumos      | Print output       |
| Alohomora  | Create variable    |
| Legilimens | Read input         |
| Reparo     | Loop               |
| Expecto    | Conditional        |
| Otherwise  | Else block         |
| EndSpell   | End block          |
| Leviosa    | Increment variable |
| Descendo   | Decrement variable |
| Hogwarts   | Select house       |

---

# 🧪 Example Program

```
Hogwarts Gryffindor

Lumos "Welcome to Hogwarts"

Alohomora counter = 1

Reparo counter until 5
    Lumos counter
    Leviosa counter
EndSpell
```

Output:

```
Welcome to Hogwarts
1
2
3
4
```

---

# 🏗 Project Architecture

```
wizardlang
│
├── core
│   ├── interpreter.py
│   ├── parser.py
│   └── environment.py
│
├── spells
│
├── houses
│
├── errors
│
├── ide
│   └── wizard_ide.py
│
└── wizard.py
```

---

# 🧙 IDE Features

The WizardLang IDE includes:

✔ Syntax highlighting
✔ Spell autocomplete
✔ Line numbers
✔ House themes
✔ File open/save
✔ Integrated interpreter
✔ Magical splash screen

---

# 🧪 Example Programs

See the **examples folder**.

```
examples/
```

---

# 🤝 Contributing

Contributions are welcome!

You can help by:

* adding new spells
* improving IDE features
* creating documentation
* fixing bugs

---

# 📜 License

MIT License

---

# ✨ Author

Created by **Chitransh**

A fun project combining **programming + creativity + the Wizarding World**.
