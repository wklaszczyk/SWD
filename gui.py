import sys
import pandas #pip install pandas
from route_data import Route
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, \
    QFileDialog, QComboBox, QLineEdit, QGroupBox, QTabWidget,QTableWidget, QLabel, QPushButton, QDialog, \
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
        self.chosen_metod = 0
        self.routes = []
        self.params = [0,0,0,0,0]

        #Stworzenie 3 boxów
        main_layout = QVBoxLayout()
        self.box_config = QGroupBox("Konfiguracja")
        layout_config = QHBoxLayout()
        self.box_ranking = QGroupBox("Ranking")
        layout_ranking = QVBoxLayout()
        self.box_routes = QGroupBox("Trasy")
        layout_routes = QHBoxLayout()

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
        self.routes_table = QTableWidget(parent)
        self.routes_table.setFixedSize(1500,400)
        self.routes_table.setColumnCount(5)
        self.routes_table.setColumnWidth(0, 150)
        self.routes_table.setColumnWidth(1, 150)
        self.routes_table.setColumnWidth(2, 50)
        self.routes_table.setColumnWidth(3, 50)
        self.routes_table.setColumnWidth(4, 50)  

        layout_routes.addWidget(self.routes_table)

        layout_add_routes = QVBoxLayout()
        #Dodawania trasy
        box_add_routes = QGroupBox()
        self.add_route_button = QPushButton("Dodaj trase")
        layout_add_routes.addWidget(self.add_route_button)
        self.add_route_button.clicked.connect(self.add_route)
        adding_route = Route(self.params[0],self.params[1],self.params[2],self.params[3],self.params[4])
        self.routes.append(adding_route)


        #Edytowanie
        self.edit_route_button = QPushButton("Edytuj trase")
        layout_add_routes.addWidget(self.edit_route_button)
        self.edit_route_button.clicked.connect(self.edit_route)

        #Usuwanie
        self.remove_route_button = QPushButton("Usuń trase")

        #Dodanie boxu tras
        layout_routes.addWidget(box_add_routes)
        box_add_routes.setLayout(layout_add_routes)
        layout_add_routes.addWidget(self.remove_route_button)

        #RANKING
        self.rank_table = QTableWidget(parent)
        self.rank_table.setFixedSize(1500,400)
        layout_ranking.addWidget(self.rank_table)


        #Dodanie odpowiednich layoutów do boxów
        self.box_config.setLayout(layout_config)
        self.box_ranking.setLayout(layout_ranking)
        self.box_routes.setLayout(layout_routes)
        
        #Dodanie boxów do głównego widoku
        main_layout.addWidget(self.box_config)
        self.box_config.setFixedHeight(70)
        main_layout.addWidget(self.box_routes)
        main_layout.addWidget(self.box_ranking)
        

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

    #Dodawanie/edytowanie trasy - okno dialogowe
    def add_route(self):
        add_dialog = QDialog()
        layout = QFormLayout()
        route_lenght = QSpinBox()
        route_lenght.setRange(0,1000)
        route_lenght.setValue(0)
        route_lenght.valueChanged.connect(self.update_lenght)
        layout.addRow("Długość trasy:",route_lenght)
        layout.addRow("Ilość poszkodowanych:",QSpinBox())
        
        add_button = QPushButton("Dodaj trase")
        add_button.clicked.connect(add_dialog.accept)
        layout.addRow(add_button)
        add_dialog.setLayout(layout)
        add_dialog.exec()

    @pyqtSlot(int)
    def update_lenght(self,lenght):
        self.params[0] = lenght

    def edit_route(self):
        edit_dialog = QDialog()
        self.layout = QFormLayout()
        self.route_lenght = QSpinBox()
        self.route_lenght.setRange(0,1000)
        self.layout.addRow("Długość trasy:",self.route_lenght)
        self.layout.addRow("Ilość poszkodowanych:",QSpinBox())

        self.add_button = QPushButton("Edytuj trase")
        self.add_button.clicked.connect(self.add)
        self.layout.addRow(self.add_button)
        edit_dialog.setLayout(self.layout)
        edit_dialog.exec()

