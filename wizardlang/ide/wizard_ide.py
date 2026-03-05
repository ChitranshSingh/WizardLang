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
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QSplitter
)

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtWidgets import QCompleter
from PyQt6.QtCore import QStringListModel
from wizardlang.core.interpreter import Interpreter
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPlainTextEdit, QWidget
from PyQt6.QtCore import QRect, QSize
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import time


class WizardSplash(QSplashScreen):

    def __init__(self):

        pixmap = QPixmap(500, 300)
        pixmap.fill(QColor("#1e1e1e"))

        super().__init__(pixmap)

        self.showMessage(
            "🧙 WizardLang\nSchool of Magical Programming",
            Qt.AlignmentFlag.AlignCenter,
            QColor("gold")
        )

class LineNumberArea(QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.codeEditor.line_number_area_paint_event(event)

class CodeEditor(QPlainTextEdit):

    def __init__(self, completer=None):
        super().__init__()
        self.completer = completer
        if self.completer:
            self.completer.setWidget(self)
            self.completer.activated.connect(self.insert_completion)

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)

    def line_number_area_width(self):

        digits = len(str(max(1, self.blockCount())))
        return 10 + digits * 7

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)

        else:
            self.lineNumberArea.update(
                0, rect.y(),
                self.lineNumberArea.width(),
                rect.height()
            )

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(),
                  self.line_number_area_width(),
                  cr.height())
        )

    def line_number_area_paint_event(self, event):

        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()

        top = int(self.blockBoundingGeometry(block).translated(
            self.contentOffset()).top())

        height = int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():

            if block.isVisible():

                number = str(block_number + 1)

                painter.setPen(QColor("#aaaaaa"))

                painter.drawText(
                    0, top,
                    self.lineNumberArea.width(),
                    height,
                    0,
                    number
                )

            block = block.next()
            top += height
            block_number += 1

    def insert_completion(self, completion):
        if not self.completer:
            return

        cursor = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        if extra <= 0:
            return
        cursor.movePosition(cursor.MoveOperation.Left)
        cursor.movePosition(cursor.MoveOperation.EndOfWord)
        cursor.insertText(completion[-extra:])
        self.setTextCursor(cursor)

    def text_under_cursor(self):
        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
                Qt.Key.Key_Enter,
                Qt.Key.Key_Return,
                Qt.Key.Key_Escape,
                Qt.Key.Key_Tab,
                Qt.Key.Key_Backtab
            ):
                event.ignore()
                return

        super().keyPressEvent(event)

        if not self.completer:
            return

        word = self.text_under_cursor()

        if len(word) < 1:
            self.completer.popup().hide()
            return

        self.completer.setCompletionPrefix(word)
        popup = self.completer.popup()
        rect = self.cursorRect()
        rect.setWidth(
            popup.sizeHintForColumn(0) +
            popup.verticalScrollBar().sizeHint().width()
        )
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        self.completer.complete(rect)
 
class StartupScreen(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Welcome Wizard")
        self.setGeometry(400, 300, 400, 200)

        layout = QVBoxLayout()

        label = QLabel(
            "🧙 Welcome to WizardLang\n"
            "School of Magical Programming"
        )

        layout.addWidget(label)

        button = QPushButton("Enter Hogwarts ⚡")
        button.clicked.connect(self.accept)

        layout.addWidget(button)

        self.setLayout(layout)

SPELL_DOCS = {
    "Lumos": "Prints output to the console.",
    "Alohomora": "Creates a variable.",
    "Expecto": "Conditional statement (if).",
    "Otherwise": "Else block of condition.",
    "EndSpell": "Ends loops or condition blocks.",
    "Reparo": "Loop structure.",
    "Leviosa": "Increment variable.",
    "Descendo": "Decrement variable.",
    "Legilimens": "Read user input.",
    "Hogwarts": "Select Hogwarts house mode."
}

class WizardIDE(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WizardLang Hogwarts IDE 🧙‍♂️")
        self.setGeometry(200, 200, 900, 650)

        main_layout = QVBoxLayout()

        title = QLabel("🏰 WizardLang Hogwarts IDE")
        main_layout.addWidget(title)

        editor_output_splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(editor_output_splitter)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_output_splitter.addWidget(splitter)

        spell_list = list(SPELL_DOCS.keys())

        model = QStringListModel()
        model.setStringList(spell_list)

        self.completer = QCompleter()
        self.completer.setModel(model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.spellbook = QListWidget()
        for spell, doc in SPELL_DOCS.items():
            item = QListWidgetItem(spell)
            item.setToolTip(doc)
            self.spellbook.addItem(item)
        self.spellbook.itemClicked.connect(self.insert_spell)
        splitter.addWidget(self.spellbook)

        # Code editor
        from PyQt6.QtWidgets import QPlainTextEdit
        self.editor = CodeEditor(self.completer)
        self.editor.setPlaceholderText("Write your spells here...")
        splitter.addWidget(self.editor)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)

        self.highlighter = SpellHighlighter(self.editor.document())

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

        # Output console
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        editor_output_splitter.addWidget(self.output)
        editor_output_splitter.setStretchFactor(0, 4)
        editor_output_splitter.setStretchFactor(1, 1)

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

    def insert_spell(self, item):
            spell = item.text()
            cursor = self.editor.textCursor()

            if spell == "Lumos":
                cursor.insertText('Lumos ""')
            elif spell == "Alohomora":
                cursor.insertText("Alohomora var = ")
            elif spell == "Expecto":
                cursor.insertText("Expecto condition\n")
            elif spell == "Reparo":
                cursor.insertText("Reparo counter until 5\n")
            else:
                cursor.insertText(spell + " ")

            self.editor.setTextCursor(cursor)
            self.editor.setFocus()

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

            self.editor.setPlainText(code)

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
                QWidget { background-color: #1e1e1e; color: #f8f8f2; }
                QPlainTextEdit { background-color: #2b2b2b; color: #f8f8f2; }
                QPushButton { background-color: #740001; color: white; }
                """)

            elif house == "Ravenclaw":

                self.setStyleSheet("""
                QWidget { background-color: #0e1a40; color: white; }
                QPlainTextEdit { background-color: #1b2a60; color: white; }
                QPushButton { background-color: #946b2d; color: white; }
                """)

            elif house == "Hufflepuff":

                self.setStyleSheet("""
                QWidget { background-color: #1e1e1e; color: #f0e68c; }
                QPlainTextEdit { background-color: #2b2b2b; color: #f0e68c; }
                QPushButton { background-color: #caa400; color: black; }
                """)

            elif house == "Slytherin":

                self.setStyleSheet("""
                QWidget { background-color: #0f2f1f; color: white; }
                QPlainTextEdit { background-color: #1a472a; color: white; }
                QPushButton { background-color: #2a623d; color: white; }
                """)

class SpellHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        def create_format(color):
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            fmt.setFontWeight(QFont.Weight.Bold)
            return fmt

        spells = {
            "Lumos": "#FFD700",
            "Alohomora": "#00BFFF",
            "Expecto": "#DA70D6",
            "Reparo": "#32CD32",
            "Hogwarts": "#FF4500",
            "Leviosa": "#7FFFD4",
            "Descendo": "#FF6347",
            "Legilimens": "#8A2BE2"
        }

        for spell, color in spells.items():
            pattern = QRegularExpression(rf"\b{spell}\b")
            self.rules.append((pattern, create_format(color)))

    def highlightBlock(self, text):

        for pattern, fmt in self.rules:

            iterator = pattern.globalMatch(text)

            while iterator.hasNext():
                match = iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()

                self.setFormat(start, length, fmt)

def main():

    app = QApplication(sys.argv)

    splash = WizardSplash()
    splash.show()

    time.sleep(2)

    window = WizardIDE()
    window.show()

    splash.finish(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
