from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class ScheduleView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Task", "Status", "Last Run", "Next Run", "Result"])
        layout.addWidget(self.table)

    def update_tasks(self, tasks: list[dict]) -> None:
        self.table.setRowCount(len(tasks))
        for r, task in enumerate(tasks):
            self.table.setItem(r, 0, QTableWidgetItem(task.get("name", "")))
            self.table.setItem(r, 1, QTableWidgetItem(task.get("status", "")))
            self.table.setItem(r, 2, QTableWidgetItem(task.get("last_run_time", "")))
            self.table.setItem(r, 3, QTableWidgetItem(task.get("next_run_time", "")))
            self.table.setItem(r, 4, QTableWidgetItem(task.get("last_result", "")))
