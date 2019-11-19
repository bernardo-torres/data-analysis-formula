
# Modulos
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


# Arquivos
from defines import*
from guiGenerated import *

# Qt
from PyQt5 import QtCore, QtWidgets
# from PyQt5 import QFileDialog

def selectFile():
    fileName, _ = QtWidgets.QFileDialog.getOpenFileName(MainWindow, "Escolha arquivo .txt",
                                                        "", "All Files (*);;Text Files (*.txt)")

    if len(fileName) > 5:
        runAnalysis(fileName)
        return fileName
    else:
        return


def listClicked(item):
    # QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())
    mult = float(ui.multiplierLineEdit.text())
    offset = float(ui.offsetLineEdit.text())
    ui.widget.mplPlot(bank[highFreqPack].time, bank[item.text()].data * mult + offset, item.text())
    print(item.text())


def clearPlots():
    ui.widget.mplClear()


def resetMultOffset():
    ui.multiplierLineEdit.setText("1")
    ui.offsetLineEdit.setText("0")


def showDialog():
    text, ok = QtWidgets.QInputDialog.getText(MainWindow, 'Input Dialog', 'Valor:')
    return text


def plotSetTitle():
    title = showDialog()
    # print(title)
    ui.widget.mplSetTitle(title)


def plotSetX():
    title = showDialog()
    ui.widget.mplSetXLabel(title)


def plotSetY():
    title = showDialog()
    ui.widget.mplSetYLabel(title)


# Roda janela
app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


bank = {}
EXT_DATA_STATUS = 0
KEY_NOT_FOUND = -1
DELIMITER = ' '
Fs = 40
Fs2 = Fs/2
Fs3 = Fs/20
T = 1/Fs
T2 = 1/Fs2
T3 = 1/Fs3
global highFreqPack, NPACK
highFreqPack = 0
NPACK = 0


def runAnalysis(file_path):
    # clearPlots()
    global highFreqPack, NPACK
    ui.listWidget.clear()
    # Abre arquivo
    #file_path = r'C:\Users\Be\github\DataAnalysisFormula\SkidPad_11_9__Pedico_2.txt'
    #file_path = selectFile()

    with open(file_path) as file_object:
        # Salva arquivo na lista lines
        lines = file_object.readlines()
    for line in lines:
        # Ignora linhas vazias
        if line != '\n':
            # Remove \n
            currentLine = line.strip()
            # Divide linha entre os campos separados por espaco
            splitLine = currentLine.split(DELIMITER)
            # Pega ordem dos dados do campo PX e armazena em dicionario
            # Campo dados no formado "PACOTEX YHz dado1 dado2..."
            if currentLine[0:6] == 'PACOTE':
                packNo = int(currentLine[6])
                Fs = float(splitLine[1])
                dataOrder = splitLine[2:-1]
                # Adiciona entrada DADOSPX no dicionario
                # contendo a linha com a informacao dos dados
                # ex bank[DADOSP2] = [oleoP fuelP...]
                bank[packNo] = pacotes(packNo, dataOrder, Fs)
                for index, x in enumerate(dataOrder, start=0):
                    # Adiciona entradas correspondentes aos dados
                    print(x, index)
                    bank[x] = dataType(packNo, index, 0, Fs)

                NPACK = int(packNo)
            elif currentLine[0:26] == 'POSICAO MAXIMA DO VOLANTE:':
                dic1['volPos'][1] = int(splitLine[4])
            elif currentLine[0:26] == 'POSICAO MINIMA DO VOLANTE:':
                dic1['volPos'][2] = int(splitLine[4])

            # Analisa linha por linha e divide conforme pacotes
            # Caso o primeiro caractere da linha seja um decimal
            if currentLine[0].isdecimal() == 1:
                if(NPACK == 0):
                    print(" TXT nao possui formado esperado ")
                    return
                # Pega o valor do primeiro caractere (ideitificador do pacote)
                currentPackNo = int(currentLine[0])
                # Medida para evitar erros, caso o identificador venha errado
                if currentPackNo <= NPACK:
                    # Converte dados separados em splitLine para inteiros
                    aux = [int(x) for x in splitLine[1: len(splitLine)]]
                    # Adiciona lista com valores da linha
                    bank[currentPackNo].packData.append(aux)
    #print(dic1['volPos'])
    lowFreqPack = 0
    lowestFreq = 1000
    highestFreq = 0
    # Varre os pacotes para achar a maior/menor frequencia e o respectivo pacote
    for entry in range(1, NPACK+1):
        if len(bank[entry].packData) != 0:
            # Transpoe vetores de dados para que cada linha corresponda um dado
            bank[entry].packData = (np.array(bank[entry].packData)).T

            if bank[entry].Fs < lowestFreq:
                lowestFreq = bank[entry].Fs
                lowFreqPack = entry

            if bank[entry].Fs > highestFreq:
                highestFreq = bank[entry].Fs
                highFreqPack = entry


    # Indice do primeiro elemento
    indexFirstElement = np.zeros(NPACK)
    firstTimeVal = bank[lowFreqPack].packData[-1][0]
    lastTimeVal = bank[lowFreqPack].packData[-1][-1]
    for entry in range(1, NPACK+1):
        if len(bank[entry].packData) != 0:
            bank[entry].calcTimeArraySize(highestFreq)
            # Acha em qual posição do vetor de tempo do pacote 1 esta o primeiro valor de
            # tempo do pacote 3
            print(entry, firstTimeVal)
            indexFirstElement[entry-1] = np.where(bank[entry].packData[-1] == firstTimeVal)[0][0]
            # print(indexFirstElement)

    indexFirstElement = indexFirstElement.astype(int)

    for entry in range(1, NPACK+1):
        if len(bank[entry].packData) != 0:
            bank[entry].loss = len(bank[entry].packData[-1])/(bank[entry].idealTimeArraySize)
            #print(str(len(bank[entry].packData[-1])) + ' ' + str(bank[entry].idealTimeArraySize))
            print('Perda pacote ' + str(entry) + ' = ' + str(bank[entry].loss))


    # Calcula tamanho ideal para os vetores
    idealTimeArraySize = (bank[lowFreqPack].idealTimeArraySize-1)*highestFreq/lowestFreq
    if (idealTimeArraySize % 2) == 1:
        idealTimeArraySize -= 1
    print('Tamanho do vetor ideal = ' + str(idealTimeArraySize))

    # Cria vetores inicializados com -20000
    for entry in range(1, NPACK+1):
        for i in bank[entry].dataOrder:
            # ver isso aqui
            bank[entry].idealTimeArraySize = int(idealTimeArraySize/(highestFreq/bank[entry].Fs))
            bank[i].data = -20000*np.ones(bank[entry].idealTimeArraySize)
        print(bank[entry].idealTimeArraySize)
    # Cria vetores com valores de tempo, em segundos
    for entry in range(1, NPACK+1):
        bank[entry].createTimeVector(firstTimeVal, lastTimeVal, highestFreq)
        # print(bank[entry].time)
        print(len(bank[entry].time))

    bank['time'] = bank[highFreqPack].time

    # Monta vetores novos do pacote 1 e 2 no tempo ideal nas posições
    # correspondentes. Caso não haja perda de pacotes, o resultado é um vetor
    # igual ao original.
    # Caso haja perda, as posições nas quais houveram perdas manterão o valor
    # de -200
    for j in range(1, NPACK+1):
        for i in range(indexFirstElement[j-1], indexFirstElement[j-1] + bank[j].idealTimeArraySize):
            if len(bank[j].packData) != 0:
                # Caso chegou no fim do array antes de chegar em idealTimeArraySize
                if i == len(bank[j].packData[-1]):
                    break
                delta = (bank[j].packData[-1][i] - firstTimeVal)/(highestFreq/bank[j].Fs)
                delta = int(delta)
                if delta == bank[j].idealTimeArraySize:
                    break
                pack1list = bank[j].dataOrder
                for entry in pack1list:
                    currentData = bank[entry]
                    currentData.data[delta] = bank[j].packData[currentData.positionInPack][i]


    #plt.plot(bank[2].time, bank['rpm'].data)


    # Interpola se achar -20000
    for entry in range(1, NPACK+1):
        if bank[entry].loss != 1:
            for dta in bank[entry].dataOrder:
                bank[dta] = linearInterp(bank[dta], -20000, bank[entry].idealTimeArraySize)


    # Interpola para colocar todos os dados na mesma base de tempo
    for j in range(1, NPACK+1):
        if len(bank[j].packData) != 0:
            if bank[j].Fs != highestFreq:
                pack2list = bank[j].dataOrder
                for entry in pack2list:
                    currentData = bank[entry]
                    currentData.data = np.interp(bank['time'], bank[j].time, currentData.data)


    # Aplica funcoes
    for i in dic1:
        aux = bank.get(i, KEY_NOT_FOUND)
        if aux != KEY_NOT_FOUND:
            if dic1[i][0] == mult:
                bank[i].data = dic1[i][0](bank[i].data, dic1[i][1], dic1[i][2])
            else:
                bank[i].data = dic1[i][0](bank[i].data, dic1[i][1], dic1[i][2], dic1[i][3], dic1[i][4])

    #plt.plot(bank[1].time, bank['volPos'].data,bank['time'].data, bank['acelY'].data*100, linewidth=0.5)

    offset = 0
    multiplier = 1

    for i in dic1:
        aux = bank.get(i, KEY_NOT_FOUND)
        if aux != KEY_NOT_FOUND:
            ui.listWidget.addItem(i)

    ui.label_6.setText("Pacote 1: " + str(round(bank[1].loss*100,2)) + '%')
    ui.label_7.setText("Pacote 2: " + str(round(bank[2].loss*100,2)) + '%')
    ui.label_8.setText("Pacote 3: " + str(round(bank[3].loss*100,2)) + '%')

# MainWindow.toolbar = NavigationToolbar(ui.widget.canvas, MainWindow, coordinates=True)
# MainWindow.addToolBar(MainWindow.toolbar)

ui.actionOpenFile.triggered.connect(selectFile)
ui.actionTitulo.triggered.connect(plotSetTitle)
ui.actionEixo_X.triggered.connect(plotSetX)
ui.actionEixo_Y.triggered.connect(plotSetY)
ui.listWidget.itemDoubleClicked.connect(listClicked)
ui.clearPlotButton.clicked.connect(clearPlots)  # botão para atualizar as portas seriis disponíveis
ui.resetButton.clicked.connect(resetMultOffset)


MainWindow.show()
sys.exit(app.exec_())
