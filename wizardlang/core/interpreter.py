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


            # --------------------------------
            # REPARO LOOP
            # --------------------------------
            if line.startswith("Reparo"):

                parts = line.replace("Reparo", "").strip().split("until")

                variable = parts[0].strip()
                limit = int(parts[1].strip())

                loop_block = []

                i += 1

                # collect loop block
                while i < len(lines) and lines[i].strip() != "EndSpell":
                    loop_block.append(lines[i])
                    i += 1

                # execute loop
                while self.env.get_variable(variable) < limit:
                    self.run(loop_block)

                i += 1
                continue


            # --------------------------------
            # CONDITIONAL SPELL
            # --------------------------------
            if line.startswith("Expecto"):

                condition = line.replace("Expecto", "", 1).strip()

                result = eval(condition, {}, self.env.variables)

                if_block = []
                else_block = []

                i += 1

                while i < len(lines) and lines[i].strip() not in ["Otherwise", "EndSpell"]:
                    if_block.append(lines[i])
                    i += 1

                if i < len(lines) and lines[i].strip() == "Otherwise":
                    i += 1

                    while i < len(lines) and lines[i].strip() != "EndSpell":
                        else_block.append(lines[i])
                        i += 1

                if result:
                    self.run(if_block)
                else:
                    self.run(else_block)

                i += 1
                continue


            # --------------------------------
            # NORMAL SPELLS
            # --------------------------------
            try:
                parse_line(line, self.env)

            except Exception as e:
                from wizardlang.errors.error_handler import handle_error
                handle_error(self.env, str(e))

            i += 1