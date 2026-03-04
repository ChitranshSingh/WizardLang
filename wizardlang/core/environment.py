from wizardlang.errors.error_handler import handle_error


class Environment:

    def __init__(self):
        self.variables = {}
        self.house = "Hogwarts"

    def set_house(self, house):
        self.house = house

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):

        if name not in self.variables:
            handle_error(self, f"Variable '{name}' not defined")
            return None

        return self.variables[name]