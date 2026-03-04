from wizardlang.core.environment import Environment
from wizardlang.core.parser import parse_line


class Interpreter:

    def __init__(self):
        self.env = Environment()

    def run(self, lines):

        i = 0

        while i < len(lines):

            line = lines[i].strip()

            if line == "" or line.startswith("#"):
                i += 1
                continue

            # ------------------------------
            # CONDITIONAL STATEMENT
            # ------------------------------

            if line.startswith("Expecto"):

                condition = line.replace("Expecto", "", 1).strip()

                condition_result = eval(condition, {}, self.env.variables)

                if_block = []
                else_block = []

                i += 1

                # collect IF block
                while i < len(lines) and lines[i].strip() not in ["Otherwise", "EndSpell"]:
                    if_block.append(lines[i])
                    i += 1

                # check for ELSE
                if i < len(lines) and lines[i].strip() == "Otherwise":
                    i += 1

                    while i < len(lines) and lines[i].strip() != "EndSpell":
                        else_block.append(lines[i])
                        i += 1

                # execute correct block
                if condition_result:
                    self.run(if_block)
                else:
                    self.run(else_block)

                i += 1
                continue

            # ------------------------------
            # NORMAL SPELLS
            # ------------------------------

            parse_line(line, self.env)

            i += 1