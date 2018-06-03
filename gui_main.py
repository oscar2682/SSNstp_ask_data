"""
GUI para determinar la magnitud de una explosion registrada
 en la estacion PPIG a partir de las relaciones encontradas
 por Cruz-Atienza et al. (2001)
Desarrollado por:
Oscar Castro Artola, Instituto de Geofisica, mayo 2018
"""
from PyQt4.QtGui import *
from my_funcs import ask_user_time,filter_one
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings
warnings.filterwarnings("ignore")


class MainWindow(QDialog):
    # MAIN FUNCTION
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle(self.tr("EXPLOSION MAGNITUDE CALCULATOR"))
#        self.resize(800,400)
        # LAYOUT
        grid = QGridLayout()
        self.setLayout(grid)
        self.figure = plt.figure(figsize=(7, 5), facecolor='w', edgecolor='k')
        self.image = QLabel(self)
        self.image.setGeometry(10, 20, 1000, 190)
        self.pixmap = QPixmap("/home/oscar/TRABAJO/POPO/EXPL_GUI/main/img/logo_cen_1.png")
        self.image.setPixmap(self.pixmap)
        self.image.show()
        # WIDGETS
        self.line_date = QLineEdit()
        self.line_date.setFixedWidth(200)
        self.bot_get_date = QPushButton("SSNstp data!\nYYYY/MO/DD, HH:MI:SS")
        self.bot_get_date.setFixedWidth(200)
        self.bot_exit = QPushButton("Salir")
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # LABEL 
        self.label = QLabel("<h1>CENAPRED <br> Caldulador de explosiones</h1>", self)

        # ADD WIDGETS
        grid.addWidget(self.label,8,1,8,2)
        grid.addWidget(self.line_date,6,1)
        grid.addWidget(self.bot_get_date,6,2)
        grid.addWidget(self.toolbar,7,2)
        grid.addWidget(self.canvas,8,2)
        grid.addWidget(self.bot_exit,9,3)
        # CONECTIONS
        self.line_date.textChanged.connect(lambda: self.line_date.text())
        self.bot_get_date.clicked.connect(self.get_date)
        self.bot_exit.clicked.connect(self.close)
    # FUNCTIONS
    def get_date(self):
        global datefile
        date = str(self.line_date.text())
        datfile = ask_user_time(date)
        print(datfile)
        filter_one(datfile)
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QApplication([])
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
