"""Runtime state container for WizardLang programs."""

from wizardlang.errors.error_handler import handle_error


class Environment:
    """Stores user variables and currently selected Hogwarts house."""

    def __init__(self):
        # A shared dictionary used by all spell handlers.
        self.variables = {}
        self.house = "Hogwarts"

    def set_house(self, house):
        """Update the active house style for future messages."""
        self.house = house

    def set_variable(self, name, value):
        """Create or update a variable in the current scope."""
        self.variables[name] = value

    def get_variable(self, name):
        """Read a variable, printing a house-themed error if missing."""
        if name not in self.variables:
            handle_error(self, f"Variable '{name}' not defined")
            return None

        return self.variables[name]
