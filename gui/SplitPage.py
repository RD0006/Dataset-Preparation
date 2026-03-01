from prepare.input import Dataset
from prepare.split import Splitter
from PyQt6.QtWidgets import *

class SplitPage(QWidget):
    def __init__(self, parent_gui):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Split Dataset"))
        layout.addStretch()
        self.setLayout(layout)