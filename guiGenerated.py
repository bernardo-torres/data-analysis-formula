# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dataAnalysisGui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from mplwidget import MPLWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1072, 662)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(20, 50, 131, 341))
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.listWidget.setDragEnabled(True)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 430, 141, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 500, 141, 16))
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(40, 450, 141, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 465, 131, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(40, 480, 131, 16))
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 0, 231, 16))
        self.label_5.setObjectName("label_5")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 231, 16))
        self.label_9.setObjectName("label_9")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(200, 0, 871, 621))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.widget = MPLWidget(self.tab)
        self.widget.setEnabled(True)
        self.widget.setGeometry(QtCore.QRect(20, 70, 841, 521))
        self.widget.setToolTipDuration(-4)
        self.widget.setObjectName("widget")
        self.resetButton = QtWidgets.QPushButton(self.tab)
        self.resetButton.setGeometry(QtCore.QRect(190, 40, 71, 21))
        self.resetButton.setObjectName("resetButton")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(60, 20, 61, 16))
        self.label.setObjectName("label")
        self.multiplierLineEdit = QtWidgets.QLineEdit(self.tab)
        self.multiplierLineEdit.setEnabled(True)
        self.multiplierLineEdit.setGeometry(QtCore.QRect(60, 40, 51, 20))
        self.multiplierLineEdit.setClearButtonEnabled(False)
        self.multiplierLineEdit.setObjectName("multiplierLineEdit")
        self.offsetLineEdit = QtWidgets.QLineEdit(self.tab)
        self.offsetLineEdit.setGeometry(QtCore.QRect(130, 40, 51, 20))
        self.offsetLineEdit.setClearButtonEnabled(False)
        self.offsetLineEdit.setObjectName("offsetLineEdit")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(140, 20, 61, 16))
        self.label_2.setObjectName("label_2")
        self.clearPlotButton = QtWidgets.QPushButton(self.tab)
        self.clearPlotButton.setGeometry(QtCore.QRect(670, 20, 101, 31))
        self.clearPlotButton.setObjectName("clearPlotButton")
        self.tabWidget.addTab(self.tab, "")
        self.Info = QtWidgets.QWidget()
        self.Info.setObjectName("Info")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.Info)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 871, 581))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.tabWidget.addTab(self.Info, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1072, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFigure = QtWidgets.QMenu(self.menubar)
        self.menuFigure.setObjectName("menuFigure")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionComo_utilizar = QtWidgets.QAction(MainWindow)
        self.actionComo_utilizar.setObjectName("actionComo_utilizar")
        self.actionTitulo = QtWidgets.QAction(MainWindow)
        self.actionTitulo.setObjectName("actionTitulo")
        self.actionEixo_X = QtWidgets.QAction(MainWindow)
        self.actionEixo_X.setObjectName("actionEixo_X")
        self.actionEixo_Y = QtWidgets.QAction(MainWindow)
        self.actionEixo_Y.setObjectName("actionEixo_Y")
        self.actionExportar_para_CSV = QtWidgets.QAction(MainWindow)
        self.actionExportar_para_CSV.setObjectName("actionExportar_para_CSV")
        self.menuFile.addAction(self.actionOpenFile)
        self.menuFile.addAction(self.actionExportar_para_CSV)
        self.menuFigure.addAction(self.actionTitulo)
        self.menuFigure.addAction(self.actionEixo_X)
        self.menuFigure.addAction(self.actionEixo_Y)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFigure.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Análise de Dados - Formula UFMG"))
        self.label_3.setText(_translate("MainWindow", "Pacotes recebidos: "))
        self.label_4.setText(_translate("MainWindow", "Número de pontos:"))
        self.label_6.setText(_translate("MainWindow", "Pacote 1:"))
        self.label_7.setText(_translate("MainWindow", "Pacote 2:"))
        self.label_8.setText(_translate("MainWindow", "Pacote 3:"))
        self.label_5.setText(_translate("MainWindow", "Clique duas vezes para plotar"))
        self.label_9.setText(_translate("MainWindow", "uas vezes novamente para remover"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.label.setText(_translate("MainWindow", "Multiplicador"))
        self.multiplierLineEdit.setText(_translate("MainWindow", "1"))
        self.offsetLineEdit.setText(_translate("MainWindow", "0"))
        self.label_2.setText(_translate("MainWindow", "Offset"))
        self.clearPlotButton.setText(_translate("MainWindow", "Limpar Figura"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "Espera-se como entrada um .txt que possua o seguinte formado nas primeiras linhas:\n"
"Nao tem ptoblema adicionar comentários ou outras linhas entre os dois ***.\n"
"As seguintes linhas sao essenciais, e devem ser mantidas exatamente da mesma forma como o exemplo abaixo:\n"
" -  Posicao maxima e minima do volante\n"
" - PACOTEN TAXA LISTADEDADOS VARIAVELTEMPORAL\n"
"As linhas que informam a ordem dos dados recebidos deve iniciar com PACOTEN, onde N é o numero do pacote. Em seguida, a taxa de envio em Hz. Depois, separadas por espacos, os nomes das variaveis, até a última variavel que é a variável de tempo\n"
"\n"
"\n"
"***\n"
"CARRO:\n"
"PISTA:\n"
"PILOTO:\n"
"TEMPERATURA AMBIENTE:\n"
"ANTIROLL:\n"
"PRESSAO PNEUS DIANTEIROS:\n"
"PRESSAO PNEUS TASEIROS:\n"
"ANGULO DE ATAQUE DA ASA:\n"
"MAPA MOTOR:\n"
"BALANCE BAR:\n"
"DIFERENCIAL:\n"
"TAXA DE AQUISICAO:\n"
"COMENTARIOS:\n"
"POSICAO MAXIMA DO VOLANTE:\n"
"POSICAO MINIMA DO VOLANTE:\n"
"SUSPENSAO:\n"
"PACOTE1 60 acelX_DD acelY_DD acelZ_DD acelX_DE acelY_DE acelZ_DE acelX_TD acelY_TD acelZ_TD acelX_TE acelY_TE acelZ_TE velDE velDD velTE velTD rpm beacon time\n"
"PACOTE2 30 tps oleoP fuelP injectors suspDE suspDD suspTE suspTD volPos correnteBat correnteVent correnteBomba frontBrakeP rearBrakeP time2\n"
"PACOTE3 10 batVoltage ect oilTemp tempDiscoDE tempDiscoDD tempDiscoTE tempDiscoTD tempVent tempBomba runners releVent releBomba mata gpsLat gpsLong gpsNS gpsEW time3\n"
"PACOTE4 30 ext1 ext2 ext3 ext4 ext5 ext6 ext7 ext8 ext9 ext10 ext11 ext12 time4\n"
"***\n"
"\n"
"1 -6750 -6750 -6750 6750 6750 6750 0 0 0 0 0 0 0 0 0 0 0 0 1302\n"
"2 0 5400 81 0 0 0 0 0 0 0 0 0 1350 18225 1302\n"
"4 0 27000 0 0 6858 0 0 1302 0 0 0 0 1302\n"
"3 0 135 0 0 0 0 0 0 0 0 1 0 0 0 0 78 69 1302\n"
"1 -7000 -7000 -7000 7000 7000 7000 0 0 0 0 0 0 0 0 0 0 0 0 1303\n"
"1 -7250 -7250 -7250 7250 7250 7250 0 0 0 0 0 0 0 0 0 0 0 0 1304\n"
"2 0 5800 87 0 0 0 0 0 0 0 0 0 1450 21025 1304\n"
"4 0 29000 0 0 7366 0 0 1304 0 0 0 0 1304\n"
"1 -7500 -7500 -7500 7500 7500 7500 0 0 0 0 0 0 0 0 0 0 0 0 1305\n"
"1 -7750 -7750 -7750 7750 7750 7750 0 0 0 0 0 0 0 0 0 0 0 0 1306\n"
"2 0 6200 93 0 0 0 0 0 0 0 0 0 1550 24025 1306\n"
"4 0 31000 0 0 7874 0 0 1306 0 0 0 0 1306\n"
"1 -8000 -8000 -8000 8000 8000 8000 0 0 0 0 0 0 0 0 0 0 0 0 1307\n"
"1 -8250 -8250 -8250 8250 8250 8250 0 0 0 0 0 0 0 0 0 0 0 0 1308\n"
"2 0 6600 99 0 0 0 0 0 0 0 0 0 1650 27225 1308\n"
"4 0 16744680 0 0 8382 0 0 1308 0 0 0 0 1308\n"
"3 0 165 0 0 0 0 0 0 0 0 1 0 0 0 0 78 69 1308\n"
"1 -8500 -8500 -8500 8500 8500 8500 0 0 0 0 0 0 0 0 0 0 0 0 1309\n"
"1 -8750 -8750 -8750 8750 8750 8750 0 0 0 0 0 0 0 0 0 0 0 0 1310\n"
"2 0 7000 105 0 0 0 0 0 0 0 0 0 1750 30625 1310"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Info), _translate("MainWindow", "Info"))
        self.menuFile.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuFigure.setTitle(_translate("MainWindow", "Figura"))
        self.actionOpenFile.setText(_translate("MainWindow", "Abrir"))
        self.actionComo_utilizar.setText(_translate("MainWindow", "Como utilizar"))
        self.actionTitulo.setText(_translate("MainWindow", "Titulo"))
        self.actionEixo_X.setText(_translate("MainWindow", "Eixo X"))
        self.actionEixo_Y.setText(_translate("MainWindow", "Eixo Y"))
        self.actionExportar_para_CSV.setText(_translate("MainWindow", "Exportar para CSV"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
