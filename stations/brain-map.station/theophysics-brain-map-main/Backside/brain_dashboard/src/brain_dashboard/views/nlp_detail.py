from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class NLPDetailView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("NLP detail view (MVP)"))
