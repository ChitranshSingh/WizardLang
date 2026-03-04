import sys
import os
import io
import contextlib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QHBoxLayout,
    QComboBox
)

from wizardlang.core.interpreter import Interpreter


class WizardIDE(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WizardLang Hogwarts IDE 🧙‍♂️")
        self.setGeometry(200, 200, 900, 650)

        main_layout = QVBoxLayout()

        title = QLabel("🏰 WizardLang Hogwarts IDE")
        main_layout.addWidget(title)

        # Code editor
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write your spells here...")
        main_layout.addWidget(self.editor)

        # Output console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        main_layout.addWidget(self.output)

        # Buttons layout
        button_layout = QHBoxLayout()

        self.run_button = QPushButton("⚡ Run Spell")
        self.run_button.clicked.connect(self.run_code)
        button_layout.addWidget(self.run_button)

        self.open_button = QPushButton("📂 Open File")
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        self.save_button = QPushButton("💾 Save File")
        self.save_button.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # House selector
        self.house_selector = QComboBox()
        self.house_selector.addItems(
            ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
        )
        self.house_selector.currentTextChanged.connect(self.apply_theme)

        main_layout.addWidget(self.house_selector)

        self.setLayout(main_layout)

        # Apply default theme
        self.apply_theme("Gryffindor")

    def run_code(self):

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
        
    def open_file(self):

            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open WizardLang File",
                "",
                "WizardLang Files (*.wzl)"
            )

            if file_path:

                with open(file_path, "r") as f:
                    code = f.read()

            self.editor.setText(code)

    def save_file(self):

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save WizardLang File",
                "",
                "WizardLang Files (*.wzl)"
            )

            if file_path:

                code = self.editor.toPlainText()

                with open(file_path, "w") as f:
                    f.write(code)

    def apply_theme(self, house):

            if house == "Gryffindor":

                self.setStyleSheet("""
                    QWidget { background-color: #7F0909; color: white; }
                    QTextEdit { background-color: #AE0001; color: white; }
                """)

            elif house == "Ravenclaw":

                self.setStyleSheet("""
                    QWidget { background-color: #0E1A40; color: white; }
                    QTextEdit { background-color: #222F5B; color: white; }
                """)

            elif house == "Hufflepuff":

                self.setStyleSheet("""
                    QWidget { background-color: #FFDB00; color: black; }
                    QTextEdit { background-color: #FFF4B2; color: black; }
                """)

            elif house == "Slytherin":

                self.setStyleSheet("""
                    QWidget { background-color: #1A472A; color: white; }
                    QTextEdit { background-color: #2A623D; color: white; }
                """)


def main():

    app = QApplication(sys.argv)

    window = WizardIDE()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()