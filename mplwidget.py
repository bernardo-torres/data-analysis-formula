# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure


class MPLWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)

        self.layout().addWidget(self.toolbar)

        self. mplSetXLabel('Tempo (s)')

        self.legendList = []

        self.dicTeste = {}
        
        

    def mplPlot(self, timeVector, dataVector, name):
        if name in self.dicTeste:
            self.dicTeste[name].remove()
            del self.dicTeste[name]
            self.legendList.remove(name)
        else:
            plotData, = self.canvas.axes.plot(timeVector, dataVector, linewidth=1)
            self.dicTeste[name] = plotData
            self.legendList.append(name)
            
        self.canvas.axes.legend(self.legendList, loc='upper right')
        self.canvas.draw()
        return self.dicTeste

    def mplClear(self):
        self.canvas.axes.cla()
        self.canvas.draw()
        self.legendList = []
        self.dicTeste.clear()

    def mplSetTitle(self, title):
        print(title)
        self.canvas.axes.set_title(title)
        self.canvas.draw()

    def mplSetXLabel(self, xlabel):
        self.canvas.axes.set_xlabel(xlabel)
        self.canvas.draw()

    def mplSetYLabel(self, ylabel):
        self.canvas.axes.set_ylabel(ylabel)
        self.canvas.draw()
