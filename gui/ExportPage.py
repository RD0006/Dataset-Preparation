from prepare.input import Dataset
from prepare.export import Exporter
from PyQt6.QtWidgets import *

class ExportPage(QWidget):
    def __init__(self, parent_gui):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Export Dataset"))
        layout.addStretch()
        self.setLayout(layout)