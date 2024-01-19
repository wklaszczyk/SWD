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
class Window(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("SWD")
        #Zmienne
        self.chosen_metod = 0;
        self.routes = [];

        #Stworzenie 3 boxów
        main_layout = QHBoxLayout()
        left_box = QGroupBox()
        self.box_config = QGroupBox("Konfiguracja")
        layout_config = QVBoxLayout()
        self.box_ranking = QGroupBox("Ranking")
        layout_ranking = QVBoxLayout()
        self.box_routes = QGroupBox("Trasy")
        layout_routes = QVBoxLayout()

        #KONFIGURACJA
        #Wczytywanie danych z pliku
        self.dane = QPushButton("Wczytaj dane z pliku")
        self.dane.clicked.connect(self.import_from_file)

        #Wybór metody
        self.cb = QComboBox()
        self.cb.addItems(["Wybierz metode","Topsis","RSM"])
        self.cb.activated.connect(self.choose_metod)

        #Rozpoczęcie algorytmu
        self.start_button = QPushButton("Stwórz ranking")
        self.start_button.resize(150,50)
        self.start_button.clicked.connect(self.start_metod)

        #Dodanie widgetów
        layout_config.addWidget(self.dane)
        layout_config.addWidget(self.cb)
        layout_config.addWidget(self.start_button)

        #TRASY
        #Wyświetlanie

        #Dodawania trasy
        self.add_route_button = QPushButton("Dodaj trase")
        layout_routes.addWidget(self.add_route_button)


        #Dodanie odpowiednich layoutów do boxów
        self.box_config.setLayout(layout_config)
        self.box_ranking.setLayout(layout_ranking)
        self.box_routes.setLayout(layout_routes)
        
        #Dodanie boxów do głównego widoku
        main_layout.addWidget(left_box)
        main_layout.addWidget(self.box_config)
        left_layout = QVBoxLayout()
        left_box.setLayout(left_layout)
        left_box.setFixedWidth(1400)
        left_layout.addWidget(self.box_routes)
        left_layout.addWidget(self.box_ranking)
        

        self.setLayout(main_layout)
        self.showMaximized()

    def choose_metod(self):
        if self.cb.currentIndex()==0:
            self.chosen_metod=0
        elif self.cb.currentIndex()==1:
            self.chosen_metod=1
        else:
            self.chosen_metod=2

    def start_metod(self):
        if len(self.routes) <2:
            QMessageBox.warning(self, "Brak danych", "Dodaj więcej tras!",
                                buttons=QMessageBox.StandardButton.Ok)
        else:         
            if self.chosen_metod==0:
                QMessageBox.warning(self, "Brak danych", "Wybierz metode!",
                                    buttons=QMessageBox.StandardButton.Ok)
            elif self.chosen_metod==1:
                pass
            elif self.chosen_metod==2:
                pass

    def import_from_file(self):
        QFileDialog.getOpenFileName(self, "Otwórz plik")[0]

    def add_route(self):
        AddDialog(self).exec()

class AddDialog(QDialog):
    def __init__(self, parent: QWidget, params, is_edit: bool = False) -> None:
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Długość trasy"))
        self.layout.addWidget(QDoubleSpinBox())
