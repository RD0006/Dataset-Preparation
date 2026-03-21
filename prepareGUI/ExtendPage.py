from prepare.input import Dataset
from prepare.extend import Extender
from PyQt6.QtWidgets import *

class ExtendPage(QWidget):
    def __init__(self, parent_gui):
        super().__init__()
        self.parent_gui = parent_gui
        self.extender = None

        layout = QVBoxLayout()
        title = QLabel("Extend Dataset")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.column_selector = QComboBox()
        layout.addWidget(QLabel("Select Column:"))
        layout.addWidget(self.column_selector)

        self.extension_selector = QComboBox()
        self.extension_selector.addItems([
            "Add Duplicate Rows",
            "Add Gaussian Rows",
            "Balance Classes",
            "Add Noise"
        ])
        layout.addWidget(QLabel("Select Extension Type:"))
        layout.addWidget(self.extension_selector)

        self.extra_input = QLineEdit()
        self.extra_input.setPlaceholderText("Optional Parameters (Comma Separated)")
        layout.addWidget(self.extra_input)
        
        self.run_button = QPushButton("Extend Dataset")
        self.run_button.clicked.connect(self.run_extension)
        layout.addWidget(self.run_button)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        layout.addStretch()
        self.setLayout(layout)
    
    def populate_columns(self):
        dataset_object = self.parent_gui.dataset
        if dataset_object:
            self.column_selector.clear()
            self.column_selector.addItems(dataset_object.columns)

    def run_extension(self):
        dataset_object = self.parent_gui.dataset
        if dataset_object is None:
            QMessageBox.warning(self, "Warning", "No Dataset Loaded")
            return
        
        column = self.column_selector.currentText()
        extension_type = self.extension_selector.currentText()
        params = [x.strip() for x in self.extra_input.text().split(",") if x.strip()]

        try:

            self.extender = Extender(dataset_object)

            if extension_type == "Add Duplicate Rows":
                self.extender.add_duplicate_rows(
                    int(params[0]) if len(params) > 0 else 10,
                    int(params[1]) if len(params) > 1 else 42
                )

            elif extension_type == "Add Gaussian Rows":
                self.extender.add_gaussian_rows(
                    int(params[0]) if len(params) > 0 else 10,
                    int(params[1]) if len(params) > 1 else 42
                )
            
            elif extension_type == "Balance Classes":
                self.extender.balance_classes(
                    column,
                    int(params[0]) if len(params) > 0 else 5,
                    int(params[1]) if len(params) > 42 else 42
                )

            elif extension_type == "Add Noise":
                self.extender.add_noisy_rows(
                    int(params[0]) if len(params) > 0 else 10,
                    int(params[1]) if len(params) > 0.01 else 0.01,
                    int(params[2]) if len(params) > 2 else 42
                )
            
            log = self.extender.get_log()
            self.log_display.clear()
            for key, value in log.items():
                self.log_display.append(f"{key} : {value}")

        except Exception as e:
            QMessageBox.critical(self, "Extension Error", str(e))