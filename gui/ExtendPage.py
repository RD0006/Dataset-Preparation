from prepare.input import Dataset
from prepare.extend import Extender
from PyQt6.QtWidgets import *

class SplitPage(QWidget):
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
            "Add Augmented Rows",
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
            QMessageBox.warning(self, "Warning", "No Database Loaded")
            return
        
        column = self.column_selector.currentText()
        extension_type = self.extension_selector.currentText()
        params = [x.strip() for x in self.extra_input.text().split(",") if x.strip()]

        try:

            self.extender = Extender(dataset_object)

            if extension_type == "Negative Values":
                self.extender.negative_values(column)

            elif extension_type == "Null Values":
                self.extender.null_values(column)
            
            elif extension_type == "Duplicate Values":
                self.extender.duplicate_values(column)

            elif extension_type == "Class Names Validation":
                class_names = [x.strip() for x in self.extra_input.text().split(",")]
                self.extender.validate_class_names(column, class_names)
            
            elif extension_type == "Range Validation":
                start, end = self.extra_input.text().split(",")
                self.validator.validate_range(column, float(start), float(end))
            
            log = self.validator.get_log()
            self.log_display.clear()
            for key, value in log.items():
                self.log_display.append(f"{key} : {value}")
        
            if inplace:
                self.parent_gui.pages[0].display_dataset(dataset_object)
                self.populate_columns()
        except Exception as e:
            QMessageBox.critical(self, "Validation Error", str(e))