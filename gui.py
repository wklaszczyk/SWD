import sys
from RSM import *
import pandas as pd #pip install pandas
from route_data import Route
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout, \
    QFileDialog, QComboBox, QLineEdit,QTableWidgetItem, QGroupBox, QTabWidget,QTableWidget, QLabel, QPushButton, QDialog, \
    QDoubleSpinBox, QSpinBox, QListWidget, QGridLayout, QRadioButton, QCheckBox, QScrollArea
from PyQt6.QtCore import pyqtSlot, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QPolygon, QPalette

# Subclass QMainWindow to customize your application's main window
class Window(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setWindowTitle("SWD")
        #Zmienne
        self.chosen_metod = 0
        self.routes = []
        self.params = [0,0,0,0,0,'']

        #Stworzenie 3 boxów
        main_layout = QVBoxLayout()
        self.box_config = QGroupBox("Konfiguracja")
        layout_config = QHBoxLayout()
        self.box_ranking = QGroupBox("Ranking")
        self.layout_ranking = QVBoxLayout()
        self.box_routes = QGroupBox("Trasy")
        layout_routes = QHBoxLayout()

        #KONFIGURACJA
        #Wczytywanie danych z pliku
        self.dane = QPushButton("Wczytaj dane z pliku")
        self.dane.clicked.connect(self.import_from_file)

        #Wybór metody
        self.cb = QComboBox()
        self.cb.addItems(["Wybierz metode","Topsis","RSM","SP"])
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
        self.routes_table.setColumnWidth(2, 200)
        self.routes_table.setColumnWidth(3, 200)
        self.routes_table.setColumnWidth(4, 200)  

        layout_routes.addWidget(self.routes_table)

        layout_add_routes = QVBoxLayout()
        #Dodawania trasy
        box_add_routes = QGroupBox()
        self.add_route_button = QPushButton("Dodaj trase")
        layout_add_routes.addWidget(self.add_route_button)
        self.add_route_button.clicked.connect(self.add_route)
        adding_route = [self.params[0],self.params[1],self.params[2],self.params[3],self.params[4]]
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


        #Dodanie odpowiednich layoutów do boxów
        self.box_config.setLayout(layout_config)
        self.box_ranking.setLayout(self.layout_ranking)
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
        elif self.cb.currentIndex()==2:
            self.chosen_metod=2
        else:
            self.chosen_metod=3

    def start_metod(self):
        if len(self.routes) <2:
            QMessageBox.warning(self, "Brak danych", "Dodaj więcej tras!",
                                buttons=QMessageBox.StandardButton.Ok)
        else:         
            if self.chosen_metod==0:
                QMessageBox.warning(self, "Brak danych", "Wybierz metode!",
                                    buttons=QMessageBox.StandardButton.Ok)
            else:
                if self.chosen_metod==1:
                    ranked_routes = []
                elif self.chosen_metod==2:
                    weights = [] #DO UZUPEŁNIENIA
                    A = [] #macierz punktów odniesienia, DO UZUPEŁNIENIA
                    try:
                        ranked_routes = RSM(A,self.routes,weights)
                    except Exception as e:
                        print("Błąd:",e)
                else:
                    ranked_routes = []
            
                if len(ranked_routes) == 0:
                    return
                '''
                self.rank_table = QTableWidget()
                self.rank_table.setFixedSize(1500,400)
                self.rank_table.setRowCount(len(ranked_routes))
                self.rank_table.setColumnCount(len(ranked_routes[0]))

                
                for i in range(ranked_routes):
                    for j in range(ranked_routes[i]):
                        if isinstance(value, (float, int)):
                            value = '{0:0,.0f}'.format(value)
                        tableItem = QTableWidgetItem(str(ranked_routes[i][j]))
                        self.rank_table.setItem(i,j,tableItem)
                
                self.layout_ranking.addWidget(self.rank_table)
                '''

    def import_from_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Otwórz plik",filter="*.xlsx")[0]
        df = pd.read_excel(file_name)
        if df.size == 0:
            return
        self.routes_table.setRowCount(df.shape[0])
        self.routes_table.setColumnCount(df.shape[1])
        self.routes_table.setHorizontalHeaderLabels(df.columns)
        
        for row in df.iterrows():
            route_parameters = []
            values = row[1]
            for col_index, value in enumerate(values):
                route_parameters.append(value)
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.routes_table.setItem(row[0], col_index, tableItem)
            self.routes.append([route_parameters[0],route_parameters[1],route_parameters[2],route_parameters[3],route_parameters[4]])

    #Dodawanie/edytowanie trasy - okno dialogowe
    def add_route(self):
        add_dialog = QDialog()
        layout = QFormLayout()
        route_lenght = QSpinBox()
        route_lenght.setRange(0,10000)
        route_lenght.setValue(0)
        route_lenght.valueChanged.connect(self.update_lenght)
        layout.addRow("Długość trasy:",route_lenght)

        route_dificulty = QSpinBox()
        route_dificulty.setRange(1,5)
        route_lenght.setValue(1)
        route_lenght.valueChanged.connect(self.update_dificulty)       
        layout.addRow("Trudność trasy:",route_dificulty)

        route_weather = QSpinBox()
        route_weather.setRange(1,5)
        route_weather.setValue(1)
        route_weather.valueChanged.connect(self.update_weather)    
        layout.addRow("Warunki atmosferyczne:",route_weather)

        route_time = QSpinBox()
        route_time.setRange(0,300)
        route_time.setValue(0)
        route_time.valueChanged.connect(self.update_time)    
        layout.addRow("Czas dotarcia:",route_time)

        route_avalanche = QSpinBox()
        route_avalanche.setRange(0,3)
        route_avalanche.setValue(0)
        route_avalanche.valueChanged.connect(self.update_avalanche)         
        layout.addRow("Zagrożenie lawinowe:",route_avalanche)

        self.route_transport = QComboBox()
        self.route_transport.addItems(['Wybierz środek transportu','Pieszo','Skuter','Narty','Helikopter'])
        self.route_transport.activated.connect(self.update_transport)           
        layout.addRow("Transport:",self.route_transport)
        
        add_button = QPushButton("Dodaj trase")
        add_button.clicked.connect(add_dialog.accept)
        layout.addRow(add_button)
        add_dialog.setLayout(layout)
        add_dialog.exec()

    @pyqtSlot(int)
    def update_lenght(self,lenght):
        self.params[0] = lenght

    def update_dificulty(self,dificulty):
        self.params[1] = dificulty

    def update_weather(self,weather):
        self.params[2] = weather

    def update_time(self,time):
        self.params[3] = time
        
    def update_avalanche(self,avalanche):
        self.params[4] = avalanche

    def update_transport(self):
        if self.route_transport.currentIndex()==1:
            self.params[5] = 'Pieszo'
        elif self.route_transport.currentIndex()==2:
            self.params[5] = 'Skuter'
        elif self.route_transport.currentIndex()==3:
            self.params[5] = 'Narty'
        elif self.route_transport.currentIndex()==4:
            self.params[5] = 'Helikopter'
        else:
            pass

    def edit_route(self):
        edit_dialog = QDialog()
        layout = QFormLayout()
        route_lenght = QSpinBox()
        route_lenght.setRange(0,10000)
        route_lenght.setValue(0)
        route_lenght.valueChanged.connect(self.update_lenght)
        layout.addRow("Długość trasy:",route_lenght)

        route_dificulty = QSpinBox()
        route_dificulty.setRange(1,5)
        route_lenght.setValue(1)
        route_lenght.valueChanged.connect(self.update_dificulty)       
        layout.addRow("Trudność trasy:",route_dificulty)

        route_weather = QSpinBox()
        route_weather.setRange(1,5)
        route_weather.setValue(1)
        route_weather.valueChanged.connect(self.update_weather)    
        layout.addRow("Warunki atmosferyczne:",route_weather)

        route_time = QSpinBox()
        route_time.setRange(0,300)
        route_time.setValue(0)
        route_time.valueChanged.connect(self.update_time)    
        layout.addRow("Czas dotarcia:",route_time)

        route_avalanche = QSpinBox()
        route_avalanche.setRange(0,3)
        route_avalanche.setValue(0)
        route_avalanche.valueChanged.connect(self.update_avalanche)         
        layout.addRow("Zagrożenie lawinowe:",route_avalanche)

        self.route_transport = QComboBox()
        self.route_transport.addItems(['Wybierz środek transportu','Pieszo','Skuter','Narty','Helikopter'])
        self.route_transport.activated.connect(self.update_transport)           
        layout.addRow("Transport:",self.route_transport)

        add_button = QPushButton("Edytuj trase")
        add_button.clicked.connect(edit_dialog.accept)
        layout.addRow(add_button)
        edit_dialog.setLayout(layout)
        edit_dialog.exec()

