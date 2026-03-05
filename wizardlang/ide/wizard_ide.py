"""WizardLang IDE built with PyQt6.

The IDE includes:
- Spellbook side panel with tooltips and click-to-insert
- Code editor with line numbers, autocomplete, and hover docs
- Output console with run + debug mode
- Hogwarts house theme switcher
"""

import contextlib
import io
import os
import sys
import time

# Allow direct script execution: python wizardlang/ide/wizard_ide.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtCore import QRegularExpression, QRect, QSize, QStringListModel, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap, QSyntaxHighlighter, QTextCharFormat
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QCompleter,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QSplashScreen,
    QTextEdit,
    QToolTip,
    QVBoxLayout,
    QWidget,
)

from wizardlang.core.interpreter import Interpreter

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
    "Hogwarts": "Select Hogwarts house mode.",
}


class WizardSplash(QSplashScreen):
    """Simple splash screen shown while the IDE starts."""

    def __init__(self):
        pixmap = QPixmap(500, 300)
        pixmap.fill(QColor("#1e1e1e"))
        super().__init__(pixmap)

        self.showMessage(
            "🧙 WizardLang\nSchool of Magical Programming",
            Qt.AlignmentFlag.AlignCenter,
            QColor("gold"),
        )


class LineNumberArea(QWidget):
    """Small widget painted beside the editor to show line numbers."""

    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """Main editor widget with line numbers, autocomplete, and hover docs."""

    def __init__(self, completer=None, spell_docs=None):
        super().__init__()
        self.completer = completer
        self.spell_docs = spell_docs or {}
        self._hovered_spell = None

        # Mouse tracking is required for hover tooltips.
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

        if self.completer:
            self.completer.setWidget(self)
            self.completer.activated.connect(self.insert_completion)

        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)

    def line_number_area_width(self):
        """Compute left margin width based on total line count."""
        digits = len(str(max(1, self.blockCount())))
        return 10 + digits * 7

    def update_line_number_area_width(self, _):
        """Reserve left space for line numbers."""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """Repaint line numbers when the editor scrolls or updates."""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0,
                rect.y(),
                self.line_number_area.width(),
                rect.height(),
            )

    def resizeEvent(self, event):
        """Keep line number area aligned with editor content."""
        super().resizeEvent(event)
        content_rect = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(
                content_rect.left(),
                content_rect.top(),
                self.line_number_area_width(),
                content_rect.height(),
            )
        )

    def line_number_area_paint_event(self, event):
        """Draw line numbers for all visible text blocks."""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor("#2b2b2b"))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        height = int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible():
                painter.setPen(QColor("#aaaaaa"))
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width(),
                    height,
                    0,
                    str(block_number + 1),
                )
            block = block.next()
            top += height
            block_number += 1

    def insert_completion(self, completion):
        """Insert selected completion text into current word."""
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
        """Get current word under the caret."""
        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()

    def _show_spell_doc_tooltip(self, event):
        """Show spell documentation when hovering a known spell."""
        cursor = self.cursorForPosition(event.position().toPoint())
        cursor.select(cursor.SelectionType.WordUnderCursor)
        hovered_word = cursor.selectedText()

        if hovered_word in self.spell_docs:
            if self._hovered_spell != hovered_word:
                tooltip_text = f"{hovered_word}\n{self.spell_docs[hovered_word]}"
                QToolTip.showText(event.globalPosition().toPoint(), tooltip_text, self)
                self._hovered_spell = hovered_word
            return

        if self._hovered_spell is not None:
            QToolTip.hideText()
            self._hovered_spell = None

    def mouseMoveEvent(self, event):
        """Track mouse movement to power hover-based spell docs."""
        self._show_spell_doc_tooltip(event)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        """Hide tooltip when cursor leaves the editor."""
        QToolTip.hideText()
        self._hovered_spell = None
        super().leaveEvent(event)

    def keyPressEvent(self, event):
        """Handle autocomplete popup behavior while typing."""
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
                Qt.Key.Key_Enter,
                Qt.Key.Key_Return,
                Qt.Key.Key_Escape,
                Qt.Key.Key_Tab,
                Qt.Key.Key_Backtab,
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
        if self.completer.completionCount() == 0:
            self.completer.popup().hide()
            return

        popup = self.completer.popup()
        rect = self.cursorRect()
        rect.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
        popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
        self.completer.complete(rect)


class StartupScreen(QDialog):
    """Optional welcome dialog (kept for future onboarding flow)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome Wizard")
        self.setGeometry(400, 300, 400, 200)

        layout = QVBoxLayout()
        layout.addWidget(
            QLabel("🧙 Welcome to WizardLang\nSchool of Magical Programming")
        )

        enter_button = QPushButton("Enter Hogwarts ⚡")
        enter_button.clicked.connect(self.accept)
        layout.addWidget(enter_button)

        self.setLayout(layout)


class WizardIDE(QWidget):
    """Main IDE window with editor, spellbook, controls, and output panel."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("WizardLang Hogwarts IDE 🧙‍♂️")
        self.setGeometry(200, 200, 950, 680)

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("🏰 WizardLang Hogwarts IDE"))

        # Vertical splitter: top (spellbook+editor) and bottom (output console).
        editor_output_splitter = QSplitter(Qt.Orientation.Vertical)
        main_layout.addWidget(editor_output_splitter)

        # Horizontal splitter: left spellbook, right editor.
        spell_editor_splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_output_splitter.addWidget(spell_editor_splitter)

        # Build autocomplete model from spell docs keys.
        model = QStringListModel()
        model.setStringList(list(SPELL_DOCS.keys()))

        self.completer = QCompleter()
        self.completer.setModel(model)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        # Left spellbook panel with hover docs.
        self.spellbook = QListWidget()
        for spell, doc in SPELL_DOCS.items():
            item = QListWidgetItem(spell)
            item.setToolTip(doc)
            self.spellbook.addItem(item)
        self.spellbook.itemClicked.connect(self.insert_spell)
        spell_editor_splitter.addWidget(self.spellbook)

        # Main code editor.
        self.editor = CodeEditor(self.completer, SPELL_DOCS)
        self.editor.setPlaceholderText("Write your spells here...")
        spell_editor_splitter.addWidget(self.editor)
        spell_editor_splitter.setStretchFactor(0, 1)
        spell_editor_splitter.setStretchFactor(1, 4)

        # Keep syntax highlighting active on the editor document.
        self.highlighter = SpellHighlighter(self.editor.document())

        # Action buttons.
        button_layout = QHBoxLayout()

        self.run_button = QPushButton("⚡ Run Spell")
        self.run_button.clicked.connect(self.run_code)
        button_layout.addWidget(self.run_button)

        self.debug_button = QPushButton("🔍 Debug Spell")
        self.debug_button.clicked.connect(self.run_debug)
        button_layout.addWidget(self.debug_button)

        self.open_button = QPushButton("📂 Open File")
        self.open_button.clicked.connect(self.open_file)
        button_layout.addWidget(self.open_button)

        self.save_button = QPushButton("💾 Save File")
        self.save_button.clicked.connect(self.save_file)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        # Bottom output console.
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        editor_output_splitter.addWidget(self.output)
        editor_output_splitter.setStretchFactor(0, 4)
        editor_output_splitter.setStretchFactor(1, 1)
        editor_output_splitter.setSizes([520, 160])

        # Theme selector.
        self.house_selector = QComboBox()
        self.house_selector.addItems(
            ["Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"]
        )
        self.house_selector.currentTextChanged.connect(self.apply_theme)
        main_layout.addWidget(self.house_selector)

        self.setLayout(main_layout)
        self.apply_theme("Gryffindor")

    def insert_spell(self, item):
        """Insert beginner-friendly templates when clicking spellbook items."""
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
            cursor.insertText(f"{spell} ")

        self.editor.setTextCursor(cursor)
        self.editor.setFocus()

    def run_debug(self):
        """Run the program in debug mode and show a line-by-line trace."""
        code = self.editor.toPlainText()
        numbered_lines = list(enumerate(code.split("\n"), start=1))

        interpreter = Interpreter()
        debug_logs = []
        buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(buffer):
                interpreter.run(
                    numbered_lines,
                    debug=True,
                    debug_printer=debug_logs.append,
                )

            program_output = buffer.getvalue().strip()
            sections = ["🔍 Debugging Spell Execution"]
            sections.append("\n".join(debug_logs) if debug_logs else "No executable spells found.")

            if program_output:
                sections.append("⚡ Program Output")
                sections.append(program_output)

            self.output.setText("\n\n".join(sections))
        except Exception as error:
            sections = ["🔍 Debugging Spell Execution"]
            if debug_logs:
                sections.append("\n".join(debug_logs))
            sections.append(f"Debug run failed: {error}")
            self.output.setText("\n\n".join(sections))

    def run_code(self):
        """Run the script normally and display stdout in the output panel."""
        code = self.editor.toPlainText()
        lines = code.split("\n")
        interpreter = Interpreter()
        buffer = io.StringIO()

        try:
            with contextlib.redirect_stdout(buffer):
                interpreter.run(lines)
            self.output.setText(buffer.getvalue())
        except Exception as error:
            self.output.setText(str(error))

    def open_file(self):
        """Load a .wzl file into the editor."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open WizardLang File",
            "",
            "WizardLang Files (*.wzl)",
        )

        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as opened_file:
            code = opened_file.read()
        self.editor.setPlainText(code)

    def save_file(self):
        """Save editor contents into a .wzl file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save WizardLang File",
            "",
            "WizardLang Files (*.wzl)",
        )

        if not file_path:
            return

        code = self.editor.toPlainText()
        with open(file_path, "w", encoding="utf-8") as saved_file:
            saved_file.write(code)

    def apply_theme(self, house):
        """Apply one of the Hogwarts color themes to the whole IDE."""
        if house == "Gryffindor":
            self.setStyleSheet(
                """
                QWidget { background-color: #1e1e1e; color: #f8f8f2; }
                QPlainTextEdit, QTextEdit, QListWidget { background-color: #2b2b2b; color: #f8f8f2; }
                QPushButton { background-color: #740001; color: white; }
                """
            )
        elif house == "Ravenclaw":
            self.setStyleSheet(
                """
                QWidget { background-color: #0e1a40; color: white; }
                QPlainTextEdit, QTextEdit, QListWidget { background-color: #1b2a60; color: white; }
                QPushButton { background-color: #946b2d; color: white; }
                """
            )
        elif house == "Hufflepuff":
            self.setStyleSheet(
                """
                QWidget { background-color: #1e1e1e; color: #f0e68c; }
                QPlainTextEdit, QTextEdit, QListWidget { background-color: #2b2b2b; color: #f0e68c; }
                QPushButton { background-color: #caa400; color: black; }
                """
            )
        elif house == "Slytherin":
            self.setStyleSheet(
                """
                QWidget { background-color: #0f2f1f; color: white; }
                QPlainTextEdit, QTextEdit, QListWidget { background-color: #1a472a; color: white; }
                QPushButton { background-color: #2a623d; color: white; }
                """
            )


class SpellHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for WizardLang spell keywords."""

    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        def create_format(color):
            text_format = QTextCharFormat()
            text_format.setForeground(QColor(color))
            text_format.setFontWeight(QFont.Weight.Bold)
            return text_format

        spell_colors = {
            "Lumos": "#FFD700",
            "Alohomora": "#00BFFF",
            "Expecto": "#DA70D6",
            "Otherwise": "#b0c4de",
            "EndSpell": "#b0c4de",
            "Reparo": "#32CD32",
            "Hogwarts": "#FF4500",
            "Leviosa": "#7FFFD4",
            "Descendo": "#FF6347",
            "Legilimens": "#8A2BE2",
        }

        for spell, color in spell_colors.items():
            pattern = QRegularExpression(rf"\b{spell}\b")
            self.rules.append((pattern, create_format(color)))

    def highlightBlock(self, text):
        """Apply highlighting rules to each block of text."""
        for pattern, text_format in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), text_format)


def main():
    """Launch splash screen and open the WizardLang IDE window."""
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
