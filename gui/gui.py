"""
gui.py

Module for building and managing the graphical user interface (GUI) using PyQt.
"""

from .InputPage import InputPage
from .ValidatePage import ValidatePage
from .CleanPage import CleanPage
from .ExtendPage import ExtendPage
from .SplitAndExportPage import SplitAndExportPage
from PyQt6.QtWidgets import *

class GUI_Class(QWidget):

    def __init__(self):
        super().__init__()

        self.dataset = None

        self.setWindowTitle("Dataset Preparation - Desktop App")

        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.addItem("Input Dataset")
        self.sidebar.addItem("Validate Dataset")
        self.sidebar.addItem("Clean Dataset")
        self.sidebar.addItem("Extend Dataset")
        self.sidebar.addItem("Split Dataset")
        self.sidebar.addItem("Export Dataset")

        self.sidebar.currentRowChanged.connect(self.display_page)

        self.stack = QStackedWidget()

        self.pages = [
            InputPage(self),
            ValidatePage(self),
            CleanPage(self),
            ExtendPage(self),
            SplitAndExportPage(self)
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        self.sidebar.setCurrentRow(0)

    def display_page(self, index):
        self.stack.setCurrentIndex(index)


class GUI:

    def __init__(self):
        self.app = QApplication([])
        self.window = GUI_Class()

    def run(self):
        self.window.showMaximized()
        self.app.exec()
        
app_instance = GUI()
app_instance.run()