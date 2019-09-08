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

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=True)
        #self.addToolBar(self.toolbar)
        self.layout().addWidget(self.toolbar)

    def mplPlot(self, timeVector, dataVector):

        self.canvas.axes.plot(timeVector, dataVector)
        self.canvas.draw()

    def mplClear(self):
        self.canvas.axes.clear()

    def mplSetTitle(self, title):
        #self.widget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.canvas.axes.set_title(title)
