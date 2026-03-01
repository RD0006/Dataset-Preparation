from prepare.validate import Validator
from PyQt6.QtWidgets import *

class ValidatePage(QWidget):

    def __init__(self, parent_gui):
        
        super().__init__()
        self.parent_gui = parent_gui
        self.validator = None
        
        layout = QVBoxLayout()
        
        title = QLabel("Validate Dataset")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.column_selector = QComboBox()
        layout.addWidget(QLabel("Select Column:"))
        layout.addWidget(self.column_selector)

        self.validation_selector = QComboBox()
        self.validation_selector.addItems([
            "Negative Values",
            "Null Values",
            "Duplicate Values",
            "Class Names Validation",
            "Range Validation"
        ])
        layout.addWidget(QLabel("Select Validation Type:"))
        layout.addWidget(self.validation_selector)

        self.extra_input = QLineEdit()
        self.extra_input.setPlaceholderText("Optional Parameters (Comma Separated)")
        layout.addWidget(self.extra_input)

        self.inplace_checkbox = QCheckBox("Apply In-Place")
        layout.addWidget(self.inplace_checkbox)

        self.run_button = QPushButton("Run Validation")
        self.run_button.clicked.connect(self.run_validation)
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
    
    def run_validation(self):
        dataset_object = self.parent_gui.dataset
        if dataset_object is None:
            QMessageBox.warning(self, "Warning", "No Database Loaded")
            return
        
        column = self.column_selector.currentText()
        validation_type = self.validation_selector.currentText()
        inplace = self.inplace_checkbox.isChecked()

        try:

            self.validator = Validator(dataset_object, inplace = inplace)

            if validation_type == "Negative Values":
                self.validator.negative_values(column)

            elif validation_type == "Null Values":
                self.validator.null_values(column)
            
            elif validation_type == "Duplicate Values":
                self.validator.duplicate_values(column)

            elif validation_type == "Class Names Validation":
                class_names = [x.strip() for x in self.extra_input.text().split(",")]
                self.validator.validate_class_names(column, class_names)
            
            elif validation_type == "Range Validation":
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