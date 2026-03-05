"""Core execution engine for WizardLang source code."""

from wizardlang.core.environment import Environment
from wizardlang.core.parser import parse_line


class Interpreter:
    """Executes WizardLang line-by-line with optional debug tracing."""

    def __init__(self):
        self.env = Environment()

    @staticmethod
    def _line_info(raw_line, fallback_line_number):
        """Normalize input into (line_number, line_text)."""
        if isinstance(raw_line, tuple) and len(raw_line) == 2:
            return raw_line[0], str(raw_line[1])
        return fallback_line_number, str(raw_line)

    @staticmethod
    def _emit_debug(debug_printer, message):
        """Send a debug message if a debug sink is configured."""
        if debug_printer:
            debug_printer(message)

    def _describe_spell_effect(self, line, spell, before_variables, before_house):
        """Build beginner-friendly debug text for normal spells."""
        known_spells = {
            "Lumos",
            "Alohomora",
            "Legilimens",
            "Leviosa",
            "Descendo",
            "Hogwarts",
        }

        if spell not in known_spells:
            return f"Unknown spell '{spell}'"

        if spell == "Lumos":
            return "Lumos executed"

        if spell == "Alohomora":
            assignment = line.replace("Alohomora", "", 1).strip()
            name = assignment.split("=", 1)[0].strip() if "=" in assignment else ""
            if name and name in self.env.variables:
                return f"Variable '{name}' set to {self.env.variables[name]!r}"
            return "Alohomora executed"

        if spell == "Leviosa":
            name = line.replace("Leviosa", "", 1).strip()
            if name in self.env.variables:
                return f"Variable '{name}' incremented to {self.env.variables[name]!r}"
            return "Leviosa executed"

        if spell == "Descendo":
            name = line.replace("Descendo", "", 1).strip()
            if name in self.env.variables:
                return f"Variable '{name}' decremented to {self.env.variables[name]!r}"
            return "Descendo executed"

        if spell == "Legilimens":
            name = line.replace("Legilimens", "", 1).strip()
            if name in self.env.variables:
                return f"Input stored in '{name}' as {self.env.variables[name]!r}"
            return "Legilimens executed"

        if spell == "Hogwarts":
            if self.env.house != before_house:
                return f"House switched to {self.env.house}"
            return "Hogwarts executed"

        if self.env.variables != before_variables:
            return f"{spell} executed and updated variables"

        return f"{spell} executed"

    def run(self, lines, debug=False, debug_printer=None):
        """Execute a list of lines, including loops and condition blocks."""
        i = 0

        while i < len(lines):
            line_number, raw_line = self._line_info(lines[i], i + 1)
            line = raw_line.strip()

            # Ignore comments and empty lines.
            if line == "" or line.startswith("#"):
                i += 1
                continue

            # -------------------------------
            # REPARO LOOP
            # -------------------------------
            if line.startswith("Reparo"):
                parts = line.replace("Reparo", "").strip().split("until")
                variable = parts[0].strip()
                limit = int(parts[1].strip())

                loop_block = []
                i += 1

                # Collect every line until EndSpell.
                while i < len(lines):
                    _, block_line = self._line_info(lines[i], i + 1)
                    if block_line.strip() == "EndSpell":
                        break
                    loop_block.append(lines[i])
                    i += 1

                if debug:
                    self._emit_debug(
                        debug_printer,
                        f"Line {line_number} -> Reparo loop on '{variable}' until {limit}",
                    )

                # Re-run loop block until variable reaches the limit.
                iteration = 0
                while self.env.get_variable(variable) < limit:
                    iteration += 1

                    if debug:
                        current_value = self.env.get_variable(variable)
                        self._emit_debug(
                            debug_printer,
                            (
                                f"Line {line_number} -> Reparo iteration {iteration} "
                                f"({variable}={current_value!r})"
                            ),
                        )

                    self.run(loop_block, debug=debug, debug_printer=debug_printer)

                i += 1
                continue

            # -------------------------------
            # EXPECTO / OTHERWISE
            # -------------------------------
            if line.startswith("Expecto"):
                condition = line.replace("Expecto", "", 1).strip()
                result = eval(condition, {}, self.env.variables)

                if_block = []
                else_block = []
                i += 1

                # Collect the Expecto body.
                while i < len(lines):
                    _, block_line = self._line_info(lines[i], i + 1)
                    if block_line.strip() in ["Otherwise", "EndSpell"]:
                        break
                    if_block.append(lines[i])
                    i += 1

                if i < len(lines):
                    _, block_line = self._line_info(lines[i], i + 1)
                else:
                    block_line = ""

                # Collect the Otherwise body if present.
                if i < len(lines) and block_line.strip() == "Otherwise":
                    i += 1
                    while i < len(lines):
                        _, else_line = self._line_info(lines[i], i + 1)
                        if else_line.strip() == "EndSpell":
                            break
                        else_block.append(lines[i])
                        i += 1

                if result:
                    if debug:
                        self._emit_debug(
                            debug_printer,
                            (
                                f"Line {line_number} -> Expecto '{condition}' is True; "
                                "executing Expecto block"
                            ),
                        )
                    self.run(if_block, debug=debug, debug_printer=debug_printer)
                else:
                    if debug:
                        self._emit_debug(
                            debug_printer,
                            (
                                f"Line {line_number} -> Expecto '{condition}' is False; "
                                "executing Otherwise block"
                            ),
                        )
                    self.run(else_block, debug=debug, debug_printer=debug_printer)

                i += 1
                continue

            # -------------------------------
            # NORMAL SPELLS
            # -------------------------------
            before_variables = dict(self.env.variables)
            before_house = self.env.house
            spell = line.split()[0]

            try:
                parse_line(line, self.env)
            except Exception as error:
                from wizardlang.errors.error_handler import handle_error

                handle_error(self.env, str(error))

            if debug:
                effect = self._describe_spell_effect(
                    line=line,
                    spell=spell,
                    before_variables=before_variables,
                    before_house=before_house,
                )
                self._emit_debug(debug_printer, f"Line {line_number} -> {effect}")

            i += 1
