from prepare.clean import Cleaner
from PyQt6.QtWidgets import *

class CleanPage(QWidget):
    
    def __init__(self, parent_gui):
        super().__init__()
        
        self.parent_gui = parent_gui
        self.cleaner = None
        
        layout = QVBoxLayout()
        
        title = QLabel("Clean Dataset")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        layout.addWidget(QLabel("Select Column:"))
        self.column_selector = QComboBox()
        layout.addWidget(self.column_selector)

        layout.addWidget(QLabel("Select Cleaning Operation:"))
        self.cleaning_selector = QComboBox()
        self.cleaning_selector.addItems([
            "Handle Missing Values",
            "Remove Duplicate Rows",
            "Handle Outliers",
            "Fix Categoricals",
            "Drop Column",
            "Normalize",
            "Standardize"
        ])
        layout.addWidget(self.cleaning_selector)

        self.extra_input = QLineEdit()
        self.extra_input.setPlaceholderText("Optional Parameters (Comma Separated)")
        layout.addWidget(self.extra_input)

        self.all_columns_checkbox = QCheckBox("Apply to All Columns")
        layout.addWidget(self.all_columns_checkbox)

        self.run_button = QPushButton("Run Cleaning")
        self.run_button.clicked.connect(self.run_cleaning)
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

    def run_cleaning(self):
        dataset_object = self.parent_gui.dataset
        if dataset_object is None:
            QMessageBox.warning(self, "Warning", "No Database Loaded")
            return
        
        column = self.column_selector.currentText()
        operation = self.cleaning_selector.currentText()
        all_columns = self.all_columns_checkbox.isChecked()

        try:

            self.cleaner = Cleaner(dataset_object)

            if operation == "Handle Missing Values":
                self.cleaner.handle_missing_values(column = None if all_columns else column)

            elif operation == "Remove Duplicate Rows":
                self.cleaner.drop_duplicate_rows()
            
            elif operation == "Handle Outliers":
                self.cleaner.handle_outliers(column = None if all_columns else column)

            elif operation == "Fix Categoricals":
                self.cleaner.fix_categoricals(column = None if all_columns else column)
            
            elif operation == "Drop Column":
                self.cleaner.drop_column(column = column)
            
            elif operation == "Normalize":
                self.cleaner.normalize(column = None if all_columns else column)

            elif operation == "Standardize":
                self.cleaner.standardize(column = None if all_columns else column)

            log = self.cleaner.get_log_of_fixed_issues()
            self.log_display.clear()
            for key, value in log.items():
                self.log_display.append(f"{key} : {value}")
        
            self.parent_gui.pages[0].display_dataset(dataset_object)
            self.populate_columns()

        except Exception as e:
            QMessageBox.critical(self, "Cleaning Error", str(e))