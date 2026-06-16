"""FIS GUI — PySide6 desktop app for file intelligence.

Universal flow: Pick items → Pick action → Pick target/name → Preview → Approve → Record

One dynamic panel reconfigures per action using ACTION_DEFS from actions.py.
"""
import sys
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTreeView, QListWidget, QListWidgetItem, QLabel,
    QPushButton, QComboBox, QLineEdit, QCheckBox, QFileDialog,
    QTextEdit, QGroupBox, QFormLayout, QTabWidget, QToolButton,
    QMessageBox, QStatusBar, QFrame,
)
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QFileSystemModel, QFont

from fis.actions import ACTION_DEFS, preview_action, execute_action


class FISWindow(QMainWindow):
    """Main FIS GUI window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("FIS — File Intelligence System")
        self.setMinimumSize(1100, 700)
        self.selected_items = []
        self.current_action = "rename"
        self.option_widgets = {}

        self._build_ui()
        self.statusBar().showMessage("Ready. Select files, pick action, preview, approve.")

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # --- Left: File browser ---
        left = QVBoxLayout()
        left_label = QLabel("📂 File Browser")
        left_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        left.addWidget(left_label)

        self.fs_model = QFileSystemModel()
        self.fs_model.setRootPath(QDir.rootPath())
        self.tree = QTreeView()
        self.tree.setModel(self.fs_model)
        self.tree.setSelectionMode(QTreeView.ExtendedSelection)
        self.tree.setColumnWidth(0, 300)
        self.tree.hideColumn(1)  # Size
        self.tree.hideColumn(2)  # Type
        left.addWidget(self.tree)

        add_btn = QPushButton("➕ Add Selected to Items")
        add_btn.clicked.connect(self._add_selected)
        left.addWidget(add_btn)

        self.items_list = QListWidget()
        self.items_list.setMaximumHeight(150)
        left.addWidget(QLabel("Selected Items:"))
        left.addWidget(self.items_list)

        clear_btn = QPushButton("Clear Items")
        clear_btn.clicked.connect(self._clear_items)
        left.addWidget(clear_btn)

        left_widget = QWidget()
        left_widget.setLayout(left)

        # --- Right: Action panel ---
        right = QVBoxLayout()

        # Action selector buttons
        action_bar = QHBoxLayout()
        self.action_buttons = {}
        for key, adef in ACTION_DEFS.items():
            btn = QPushButton(f"{adef['icon']} {adef['label']}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, k=key: self._select_action(k))
            action_bar.addWidget(btn)
            self.action_buttons[key] = btn
        right.addLayout(action_bar)

        # Purpose label
        self.purpose_label = QLabel("")
        self.purpose_label.setStyleSheet("color: #666; font-style: italic;")
        right.addWidget(self.purpose_label)

        # Dynamic options area
        self.options_group = QGroupBox("Options")
        self.options_layout = QFormLayout()
        self.options_group.setLayout(self.options_layout)
        right.addWidget(self.options_group)

        # Preview / Approve buttons
        btn_row = QHBoxLayout()
        preview_btn = QPushButton("👁️ Preview")
        preview_btn.setStyleSheet("font-size: 14px; padding: 8px 20px;")
        preview_btn.clicked.connect(self._preview)
        btn_row.addWidget(preview_btn)

        approve_btn = QPushButton("✅ Approve")
        approve_btn.setStyleSheet("font-size: 14px; padding: 8px 20px; background: #2d7d46; color: white;")
        approve_btn.clicked.connect(self._approve)
        btn_row.addWidget(approve_btn)
        right.addLayout(btn_row)

        # Preview output area
        self.preview_output = QTextEdit()
        self.preview_output.setReadOnly(True)
        self.preview_output.setPlaceholderText("Preview will appear here...")
        self.preview_output.setFont(QFont("Consolas", 10))
        right.addWidget(self.preview_output)

        right_widget = QWidget()
        right_widget.setLayout(right)

        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([350, 750])
        main_layout.addWidget(splitter)

        # Initialize with rename action
        self._select_action("rename")

    # --- Slots ---

    def _add_selected(self):
        indexes = self.tree.selectionModel().selectedIndexes()
        added = set()
        for idx in indexes:
            if idx.column() == 0:  # Name column only
                path = self.fs_model.filePath(idx)
                if path not in added and path not in self.selected_items:
                    self.selected_items.append(path)
                    self.items_list.addItem(QListWidgetItem(path))
                    added.add(path)
        self.statusBar().showMessage(f"{len(self.selected_items)} items selected")

    def _clear_items(self):
        self.selected_items.clear()
        self.items_list.clear()
        self.statusBar().showMessage("Items cleared")

    def _select_action(self, action_key: str):
        self.current_action = action_key
        adef = ACTION_DEFS[action_key]
        # Toggle button states
        for k, btn in self.action_buttons.items():
            btn.setChecked(k == action_key)
        self.purpose_label.setText(f"{adef['icon']} {adef['purpose']}")
        self.options_group.setTitle(f"{adef['label']} Options")
        self._build_options(adef["options"])
        self.preview_output.clear()
        self.statusBar().showMessage(f"Action: {adef['label']}")

    def _build_options(self, option_defs: list[dict]):
        """Dynamically build form fields from action definition."""
        # Clear existing
        while self.options_layout.count():
            item = self.options_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.option_widgets.clear()

        for opt in option_defs:
            key = opt["key"]
            label = opt["label"]
            opt_type = opt["type"]

            if opt_type == "choice":
                w = QComboBox()
                for c in opt.get("choices", []):
                    w.addItem(c.replace('_', ' ').title(), c)
            elif opt_type == "text":
                w = QLineEdit()
                w.setPlaceholderText(f"Enter {label.lower()}...")
            elif opt_type == "bool":
                w = QCheckBox()
                w.setChecked(opt.get("default", False))
            elif opt_type == "folder_picker":
                container = QWidget()
                hl = QHBoxLayout(container)
                hl.setContentsMargins(0, 0, 0, 0)
                le = QLineEdit()
                le.setPlaceholderText("Select folder...")
                browse = QPushButton("Browse...")
                browse.clicked.connect(lambda _, line=le: self._pick_folder(line))
                hl.addWidget(le)
                hl.addWidget(browse)
                w = container
                # Store the line edit, not container, for value retrieval
                self.option_widgets[key] = le
                self.options_layout.addRow(label + ":", w)
                continue
            elif opt_type == "multi_choice":
                container = QWidget()
                hl = QHBoxLayout(container)
                hl.setContentsMargins(0, 0, 0, 0)
                checks = {}
                for c in opt.get("choices", []):
                    cb = QCheckBox(c.replace('_', ' ').title())
                    cb.setChecked(True)
                    hl.addWidget(cb)
                    checks[c] = cb
                w = container
                self.option_widgets[key] = checks
                self.options_layout.addRow(label + ":", w)
                continue
            else:
                w = QLineEdit()

            self.option_widgets[key] = w
            self.options_layout.addRow(label + ":", w)

    def _pick_folder(self, line_edit: QLineEdit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit.setText(folder)

    def _gather_options(self) -> dict:
        """Collect current option values from widgets."""
        opts = {}
        for key, w in self.option_widgets.items():
            if isinstance(w, QComboBox):
                opts[key] = w.currentData() or w.currentText()
            elif isinstance(w, QLineEdit):
                opts[key] = w.text()
            elif isinstance(w, QCheckBox):
                opts[key] = w.isChecked()
            elif isinstance(w, dict):  # multi_choice
                opts[key] = [k for k, cb in w.items() if cb.isChecked()]
        return opts

    def _preview(self):
        if not self.selected_items:
            self.statusBar().showMessage("No items selected!")
            return
        opts = self._gather_options()
        result = preview_action(self.current_action, self.selected_items, opts)
        self._show_preview(result)

    def _show_preview(self, result):
        lines = [f"=== PREVIEW: {self.current_action.upper()} ===", ""]
        for op in result.operations:
            op_type = op.get("op", "?")
            src = op.get("src", "")
            dst = op.get("dst", "")
            if dst:
                lines.append(f"  {op_type}: {Path(src).name}  →  {dst}")
            else:
                lines.append(f"  {op_type}: {Path(src).name}")
        if result.errors:
            lines.append("")
            lines.append("ERRORS:")
            for e in result.errors:
                lines.append(f"  ⚠ {e}")
        lines.append("")
        lines.append(f"Total operations: {len(result.operations)}")
        self.preview_output.setText("\n".join(lines))
        self.statusBar().showMessage(f"Preview: {len(result.operations)} operations")

    def _approve(self):
        if not self.selected_items:
            self.statusBar().showMessage("No items selected!")
            return
        reply = QMessageBox.question(
            self, "Approve Action",
            f"Execute {self.current_action.upper()} on {len(self.selected_items)} items?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        opts = self._gather_options()
        result = execute_action(self.current_action, self.selected_items, opts)
        self._show_preview(result)
        if result.success:
            self.statusBar().showMessage(
                f"✅ {self.current_action.upper()} complete — {len(result.operations)} operations recorded")
            self._clear_items()
        else:
            self.statusBar().showMessage(
                f"⚠ {self.current_action.upper()} completed with {len(result.errors)} errors")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = FISWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
