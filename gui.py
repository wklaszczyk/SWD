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
        self.routes_table.setColumnWidth(5, 100)

        layout_routes.addWidget(self.routes_table)

        layout_add_routes = QVBoxLayout()
        #Dodawania trasy
        box_add_routes = QGroupBox()
        self.add_route_button = QPushButton("Dodaj trase")
        layout_add_routes.addWidget(self.add_route_button)
        self.add_route_button.clicked.connect(self.add_route)

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
                    weights = [0.6, 0.5, 0.5, 0.9, 1, 3] #DO UZUPEŁNIENIA
                    A = [[[0, 0, 0, 0, -1, 0]],
                        [[5000, 6, 6, 120, 4, 5]]] #macierz punktów odniesienia, DO UZUPEŁNIENIA
                    ranked_routes = RSM(A,self.routes,weights)
                else:
                    ranked_routes = []
            
                if len(ranked_routes) == 0:
                    return
                
                self.rank_table = QTableWidget()
                self.rank_table.setFixedSize(1500,400)
                self.rank_table.setRowCount(len(ranked_routes)+1)
                self.rank_table.setColumnCount(len(ranked_routes[0][0])+1)
                
                for i in range(len(ranked_routes)):
                    for j in range(len(ranked_routes[i][0])):
                        if j==5:
                            if ranked_routes[i][0][j]==1:
                                value = 'Pieszo'
                            elif ranked_routes[i][0][j]==2:
                                value = 'Narty'
                            elif ranked_routes[i][0][j]==3:
                                value = "Skuter"
                            else:
                                value = "Helikopter"
                        else:
                            value = ranked_routes[i][0][j]
                        if isinstance(value, (float, int)):
                            value = '{0:0,.0f}'.format(value)
                        tableItem = QTableWidgetItem(str(value))
                        self.rank_table.setItem(i,j,tableItem)
                    value = ranked_routes[i][1]
                    tableItem = QTableWidgetItem(str(value))
                    self.rank_table.setItem(i,j+1,tableItem)
                
                self.rank_table.setColumnWidth(0, 150)
                self.rank_table.setColumnWidth(1, 150)
                self.rank_table.setColumnWidth(2, 200)
                self.rank_table.setColumnWidth(3, 200)
                self.rank_table.setColumnWidth(4, 200)
                self.rank_table.setColumnWidth(5, 100)
                self.rank_table.setColumnWidth(6, 200)
                self.layout_ranking.addWidget(self.rank_table)
                
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
                if isinstance(value, str):
                    if value=="Helikopter":
                        route_parameters.append(4)
                    elif value=="Skuter":
                        route_parameters.append(3)
                    elif value=="Narty":
                        route_parameters.append(2)
                    else:
                        route_parameters.append(1)
                else:
                    route_parameters.append(value)
                    value = '{0:0,.0f}'.format(value)
                tableItem = QTableWidgetItem(str(value))
                self.routes_table.setItem(row[0], col_index, tableItem)
            if row!=0:
                self.routes.append([route_parameters[0],route_parameters[1],route_parameters[2],route_parameters[3],route_parameters[4],route_parameters[5]])

    #Dodawanie/edytowanie trasy - okno dialogowe
    def add_route(self):
        self.params = [0,0,0,0,0,'']
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
        self.route_transport.addItems(['Wybierz środek transportu','Pieszo','Narty','Skuter','Helikopter'])
        self.route_transport.activated.connect(self.update_transport)           
        layout.addRow("Transport:",self.route_transport)

        add_button = QPushButton("Dodaj trase")
        add_button.clicked.connect(self.add)
        add_button.clicked.connect(add_dialog.accept)
        layout.addRow(add_button)
        add_dialog.setLayout(layout)
        add_dialog.exec()

    def add(self):
        adding_route = [self.params[0],self.params[1],self.params[2],self.params[3],self.params[4],self.params[5]]
        self.routes.append(adding_route)
        self.routes_table.setRowCount(len(self.routes))
        for i in range(len(adding_route)):
            if i == 5:
                if adding_route[i] == 1:
                    table_item = 'Pieszo'
                elif adding_route[i] == 2:
                    table_item = 'Narty'
                elif adding_route[i] == 3:
                    table_item = 'Skuter'
                else:
                    table_item = 'Helikopter'
                table_item = QTableWidgetItem(table_item) 
            else:
                table_item = QTableWidgetItem(str(adding_route[i]))
            self.routes_table.setItem(len(self.routes)-1,i,table_item)

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
            self.params[5] = 1
        elif self.route_transport.currentIndex()==2:
            self.params[5] = 2
        elif self.route_transport.currentIndex()==3:
            self.params[5] = 3
        elif self.route_transport.currentIndex()==4:
            self.params[5] = 4
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
        route_dificulty.setValue(1)
        route_dificulty.valueChanged.connect(self.update_dificulty)       
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

