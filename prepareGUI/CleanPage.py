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
            QMessageBox.warning(self, "Warning", "No Dataset Loaded")
            return
        
        column = self.column_selector.currentText()
        operation = self.cleaning_selector.currentText()
        all_columns = self.all_columns_checkbox.isChecked()

        if all_columns:
            column = None

        try:

            self.cleaner = Cleaner(dataset_object)

            if operation == "Handle Missing Values":
                self.cleaner.handle_missing_values(column = column, all_columns = all_columns)

            elif operation == "Remove Duplicate Rows":
                self.cleaner.drop_duplicate_rows()
            
            elif operation == "Handle Outliers":
                self.cleaner.handle_outliers(column = column, all_columns = all_columns)

            elif operation == "Fix Categoricals":
                self.cleaner.fix_categoricals(column = column, all_columns = all_columns)
            
            elif operation == "Drop Column":
                self.cleaner.drop_column(column = column, all_columns = all_columns)
            
            elif operation == "Normalize":
                self.cleaner.normalize(column = column, all_columns = all_columns)

            elif operation == "Standardize":
                self.cleaner.standardize(column = column, all_columns = all_columns)

            log = self.cleaner.get_log_of_fixed_issues()
            self.log_display.clear()
            target_column = "All Columns" if all_columns else column

            self.log_display.append(f"Target Column(s): {target_column}\n")
            for key, value in log.items():
                self.log_display.append(f"{key} : {value}")
        
            self.parent_gui.pages[0].display_dataset(dataset_object)
            self.populate_columns()

        except Exception as e:
            QMessageBox.critical(self, "Cleaning Error", str(e))