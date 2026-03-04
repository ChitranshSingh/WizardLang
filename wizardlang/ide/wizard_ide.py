import sys
import os
# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import io
import contextlib
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel
)


class WizardIDE(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WizardLang IDE 🧙‍♂️")
        self.setGeometry(200, 200, 800, 600)

        layout = QVBoxLayout()

        title = QLabel("WizardLang Hogwarts IDE")
        layout.addWidget(title)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your spells here...")
        layout.addWidget(self.editor)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.run_button = QPushButton("⚡ Run Spell")
        self.run_button.clicked.connect(self.run_code)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def run_code(self):

        from wizardlang.core.interpreter import Interpreter

        code = self.editor.toPlainText()

        lines = code.split("\n")

        interpreter = Interpreter()

        buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(buffer):
                interpreter.run(lines)


            output = buffer.getvalue()

            self.output.setText(output)

        except Exception as e:
            self.output.setText(str(e))


def main():

    app = QApplication(sys.argv)

    window = WizardIDE()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()