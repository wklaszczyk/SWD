import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, \
    QFileDialog, QComboBox, QLineEdit, QGroupBox, QTabWidget, QLabel, QPushButton, QDialog, \
    QDoubleSpinBox, QSpinBox, QListWidget, QGridLayout, QRadioButton, QCheckBox, QScrollArea
from PyQt6.QtCore import pyqtSlot, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPolygon, QPalette
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt
import matplotlib


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SWD")

        main_layout = QHBoxLayout()

        self.cb = QComboBox()
        self.cb.addItem("Wybierz metode")
        self.cb.addItem("Topsis")
        self.cb.addItem("RSM")

        main_layout.addWidget(self.cb)
        main_layout.addWidget(QPushButton("Ranking"))

        self.config = Config(self)
        self.config.setLayout(main_layout)

        self.setCentralWidget(self.config)

class Config(QWidget):
    def __init__(self, parent: MainWindow):
        super(Config, self).__init__()

        self.parent = parent

        layout_main = QFormLayout()

'''
class Ranking(QWidget):
    def __init__(self, parent: MainWindow):
        super(Ranking, self).__init__()

        self.parent = parent
'''