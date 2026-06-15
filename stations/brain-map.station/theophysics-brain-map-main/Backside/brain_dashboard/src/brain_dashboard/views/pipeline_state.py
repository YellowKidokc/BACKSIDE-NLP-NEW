from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class PipelineStateView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Pipeline state view (MVP)"))
