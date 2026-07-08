from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class LogsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        layout.addWidget(self.text)

    def update_lines(self, lines: list[str]) -> None:
        self.text.setPlainText("\n".join(lines))
