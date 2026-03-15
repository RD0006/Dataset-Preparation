from prepare.input import Dataset
from prepare.split import Splitter
from prepare.export import Exporter
from PyQt6.QtWidgets import *

class SplitAndExportPage(QWidget):
    def __init__(self, parent_gui):
        super().__init__()
        self.parent_gui = parent_gui
        self.splitter = None
        self.result = None

        layout = QVBoxLayout()
        title = QLabel("Split and Export Dataset")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.split_selector = QComboBox()
        self.split_selector.addItems([
            "No Split",
            "Split into train and test Datasets",
            "Split into train, validate, and test Datasets"
        ])
        layout.addWidget(QLabel("Select Split Type:"))
        layout.addWidget(self.split_selector)

        self.extra_input_1 = QLineEdit()
        self.extra_input_1.setPlaceholderText("Ratio")
        layout.addWidget(self.extra_input_1)

        self.shuffle_checkbox = QCheckBox("Shuffle")
        layout.addWidget(self.shuffle_checkbox)
        
        self.split_button = QPushButton("Split Dataset")
        self.split_button.clicked.connect(self.run_split)
        layout.addWidget(self.split_button)

        self.export_selector = QComboBox()
        self.export_selector.addItems([
            "CSV",
            "JSON",
            "Parquet",
            "Excel File"
        ])
        layout.addWidget(QLabel("Select Export Format:"))
        layout.addWidget(self.export_selector)

        self.extra_input_2 = QLineEdit()
        self.extra_input_2.setPlaceholderText("Base Filename")
        layout.addWidget(self.extra_input_2)

        self.overwrite_checkbox = QCheckBox("Overwrite")
        layout.addWidget(self.overwrite_checkbox)
        
        self.export_button = QPushButton("Export Dataset")
        self.export_button.clicked.connect(self.run_export)
        layout.addWidget(self.export_button)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        layout.addStretch()
        self.setLayout(layout)

    def run_split(self):
        dataset_object = self.parent_gui.dataset
        if dataset_object is None:
            QMessageBox.warning(self, "Warning", "No Dataset Loaded")
            return
        
        split_type = self.split_selector.currentText()
        shuffle = self.shuffle_checkbox.isChecked()

        try:
            params = [float(x.strip()) for x in self.extra_input_1.text().split(",") if x.strip()]
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please provide float values for split ratio!")
            return

        try:
            self.splitter = Splitter(dataset_object)

            if split_type == "No Split":
                self.result = self.splitter.no_split(shuffle = shuffle)

            elif split_type == "Split into train and test Datasets":
                if len(params) > 0:
                    train = params[0]
                    if len(params) > 1:
                        test = params[1]
                        self.result = self.splitter.train_test(train, test, shuffle = shuffle)
                    else:
                        self.result = self.splitter.train_test(train, shuffle = shuffle)
                else:
                    QMessageBox.warning(self, "Warning", "Please provide split ratios!")
                    return
        
            elif split_type == "Split into train, validate, and test Datasets":
                if len(params) > 1:
                    train = params[0]
                    validate = params[1]
                    if len(params) > 2:
                        test = params[2]
                        self.result = self.splitter.train_validate_test(train, validate, test, shuffle = shuffle)
                    else:
                        self.result = self.splitter.train_validate_test(train, validate, shuffle = shuffle)
                else:
                    QMessageBox.warning(self, "Warning", "Please provide split ratios!")
                    return
            
            log = self.splitter.get_log()
            self.log_display.clear()
            for key, value in log.items():
                self.log_display.append(f"{key} : {value}")

        except Exception as e:
            QMessageBox.critical(self, "Splitting Error", str(e))
            return
    
    def run_export(self):
        dataset_object = self.parent_gui.dataset
        if dataset_object is None:
            QMessageBox.warning(self, "Warning", "No Dataset Loaded")
            return
        
        if self.result is None:
            QMessageBox.warning(self, "Warning", "Dataset not Split!")
            return
        
        export_type = self.export_selector.currentText()
        params = [x.strip() for x in self.extra_input_2.text().split(",") if x.strip()]
        filename = params[0] if len(params) > 0 else "dataset"
        overwrite = self.overwrite_checkbox.isChecked()
        
        try:

            self.exporter = Exporter()

            if export_type == "CSV":
                for key, value in self.result.items():
                    if key == "dataset":
                        temp = f"{filename}.csv"
                    else:
                        temp = f"{filename}_{key}.csv"
                    self.exporter.export_to_csv(value, temp, overwrite)
                    self.log_display.append(f"{temp} created!")

            elif export_type == "JSON":
                for key, value in self.result.items():
                    if key == "dataset":
                        temp = f"{filename}.json"
                    else:
                        temp = f"{filename}_{key}.json"
                    self.exporter.export_to_json(value, temp, overwrite)
                    self.log_display.append(f"{temp} created!")

            elif export_type == "Parquet":
                for key, value in self.result.items():
                    if key == "dataset":
                        temp = f"{filename}.parquet"
                    else:
                        temp = f"{filename}_{key}.parquet"
                    self.exporter.export_to_parquet(value, temp, overwrite)
                    self.log_display.append(f"{temp} created!")

            elif export_type == "Excel File":
                for key, value in self.result.items():
                    if key == "dataset":
                        temp = f"{filename}.xlsx"
                    else:
                        temp = f"{filename}_{key}.xlsx"
                    self.exporter.export_to_excel(value, temp, overwrite)
                    self.log_display.append(f"{temp} created!")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))
            return 