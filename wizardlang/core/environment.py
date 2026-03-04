class Environment:

    def __init__(self):
        self.variables = {}
        self.house = "Hogwarts"

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        if name not in self.variables:
            raise Exception(f"Variable '{name}' not defined")
        return self.variables[name]