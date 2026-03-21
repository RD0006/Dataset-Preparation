from prepare.input import Dataset
from PyQt6.QtWidgets import *

class InputPage(QWidget):
    def __init__(self, parent_gui):
        super().__init__()

        self.parent_gui = parent_gui

        layout = QVBoxLayout()

        title = QLabel("Input Dataset")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.upload_button = QPushButton("Upload Dataset")
        self.upload_button.clicked.connect(self.load_dataset)
        layout.addWidget(self.upload_button)

        self.info_label = QLabel("No Dataset Loaded")
        layout.addWidget(self.info_label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        layout.addStretch()
        self.setLayout(layout)
    
    def load_dataset(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Dataset",
            "",
            "Data Files (*.csv *.xlsx *.json *.parquet)"
        )

        if not file_path:
            return
        
        try:
            dataset_object = Dataset(file_path)

            self.parent_gui.dataset = dataset_object

            self.display_dataset(dataset_object)

            for page in self.parent_gui.pages:
                if hasattr(page, "populate_columns"):
                    page.populate_columns()

        except Exception as e:
            QMessageBox.critical(self, "Dataset Error", str(e))
    
    def display_dataset(self, dataset_object):
        dataset = dataset_object.dataset

        preview_rows = min(100, dataset_object.num_of_rows)

        self.table.setRowCount(preview_rows)
        self.table.setColumnCount(dataset_object.num_of_columns)
        self.table.setHorizontalHeaderLabels(dataset_object.columns)

        for row in range(preview_rows):
            for col in range(dataset_object.num_of_columns):
                value = str(dataset.iat[row, col])
                self.table.setItem(row, col, QTableWidgetItem(value))

        self.info_label.setText(
            f"Rows: {dataset_object.num_of_rows} | Columns: {dataset_object.num_of_columns}"
        )