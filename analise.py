
# Modulos
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas as pd


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
    # QMessageBox.information(self, "ListWidget", "You clicked: "+item.text
    global dataDictionary
    mult = float(ui.multiplierLineEdit.text())
    offset = float(ui.offsetLineEdit.text())
    name = item.text()
    data = bank[item.text()].data * mult + offset
    if name in dataDictionary:
        #dataDictionary[name].remove()
        del dataDictionary[name]

    else:
        dataDictionary[name] = data

    ui.widget.mplPlot(bank[highFreqPack].time, data, name)
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


def exportToCSV():
    global bank, dataDictionary
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(MainWindow, "Escolha pasta e nome do arquivo csv",
                                                        "", 'CSV(*.csv)')
    timeVector = bank['time']
    df = pd.DataFrame(data=dataDictionary, index=timeVector)
    df.index.name = 'Tempo'
    print(fileName)
    df.to_csv(fileName)


# app.setStyle("fusion")



EXT_DATA_STATUS = 0
KEY_NOT_FOUND = -1
DELIMITER = ' '
#Fs = 40
#Fs2 = Fs/2
#Fs3 = Fs/20
#T = 1/Fs
#T2 = 1/Fs2
#T3 = 1/Fs3
global highFreqPack, NPACK, bank
bank = {}
highFreqPack = 0
NPACK = 0
dataDictionary = {}


def runAnalysis(file_path):
    global highFreqPack, NPACK, bank, dataDictionary
    receivedPacks = []
    NPACK = 0
    bank = {}
    dataDictionary = {}
    clearPlots()

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

                NPACK += 1
                receivedPacks.append(packNo)
            elif currentLine[0:26] == 'POSICAO MAXIMA DO VOLANTE:' and len(splitLine)>4:
                dic1['volPos'][1] = int(splitLine[4])
            elif currentLine[0:26] == 'POSICAO MINIMA DO VOLANTE:' and len(splitLine)>4:
                dic1['volPos'][2] = int(splitLine[4])
            elif currentLine[0:31] == 'POSICAO MAXIMA DA SUSPENSAO DD:'and len(splitLine)>5:
                dic1['suspDD'][1] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MINIMA DA SUSPENSAO DD:' and len(splitLine)>5:
                dic1['suspDD'][2] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MAXIMA DA SUSPENSAO DE:' and len(splitLine)>5:
                dic1['suspDE'][1] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MINIMA DA SUSPENSAO DE:' and len(splitLine)>5:
                dic1['suspDE'][2] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MAXIMA DA SUSPENSAO TD:' and len(splitLine)>5:
                dic1['suspTD'][1] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MINIMA DA SUSPENSAO TD:' and len(splitLine)>5:
                dic1['suspTD'][2] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MAXIMA DA SUSPENSAO TE:' and len(splitLine)>5:
                dic1['suspTE'][1] = int(splitLine[5])
            elif currentLine[0:31] == 'POSICAO MINIMA DA SUSPENSAO TE:' and len(splitLine)>5:
                dic1['suspTE'][2] = int(splitLine[5])

            # Analisa linha por linha e divide conforme pacotes
            # Caso o primeiro caractere da linha seja um decimal
            if currentLine[0].isdecimal() == 1:
                if(NPACK == 0):
                    print(" TXT nao possui formado esperado ")
                    return
                # Pega o valor do primeiro caractere (ideitificador do pacote)
                currentPackNo = int(currentLine[0])
                # Medida para evitar erros, caso o identificador venha errado
                if currentPackNo in receivedPacks:
                    # Converte dados separados em splitLine para inteiros
                    aux = [int(x) for x in splitLine[1: len(splitLine)]]
                    # Adiciona lista com valores da linha
                    bank[currentPackNo].packData.append(aux)
    #print(dic1['volPos'])
    lowFreqPack = 0
    lowestFreq = 1000
    highestFreq = 0
    # Varre os pacotes para achar a maior/menor frequencia e o respectivo pacote
    for pack in receivedPacks:
        if len(bank[pack].packData) != 0:
            # Transpoe vetores de dados para que cada linha corresponda um dado
            bank[pack].packData = (np.array(bank[pack].packData)).T

            if bank[pack].Fs < lowestFreq:
                lowestFreq = bank[pack].Fs
                lowFreqPack = pack

            if bank[pack].Fs > highestFreq:
                highestFreq = bank[pack].Fs
                highFreqPack = pack


    # Indice do primeiro elemento
    indexFirstElement = np.zeros(NPACK)
    firstTimeVal = bank[lowFreqPack].packData[-1][0]
    lastTimeVal = bank[lowFreqPack].packData[-1][-1]
    for pack in receivedPacks:
        if len(bank[pack].packData) != 0:
            bank[pack].calcTimeArraySize(highestFreq)
            # Acha em qual posição do vetor de tempo do pacote 1 esta o primeiro valor de
            # tempo do pacote 3
            print(pack, firstTimeVal)
            newFirstValue = np.where(bank[pack].packData[-1] == firstTimeVal)
            if newFirstValue[0].size > 0:
                indexFirstElement[pack-1] =  newFirstValue[0][0]
            else:
                index = np.searchsorted(bank[pack].packData[-1], firstTimeVal)
                bank[pack].packData[-1][index] = firstTimeVal


    indexFirstElement = indexFirstElement.astype(int)

    for pack in receivedPacks:
        if len(bank[pack].packData) != 0:
            bank[pack].loss = len(bank[pack].packData[-1])/(bank[pack].idealTimeArraySize)
            #print(str(len(bank[entry].packData[-1])) + ' ' + str(bank[entry].idealTimeArraySize))
            print('Perda pacote ' + str(pack) + ' = ' + str(bank[pack].loss))


    # Calcula tamanho ideal para os vetores
    idealTimeArraySize = (bank[lowFreqPack].idealTimeArraySize-1)*highestFreq/lowestFreq
    if (idealTimeArraySize % 2) == 1:
        idealTimeArraySize -= 1

    print('Tamanho do vetor ideal = ' + str(idealTimeArraySize))


    # Cria vetores inicializados com -20000
    for pack in receivedPacks:
        for i in bank[pack].dataOrder:
            # ver isso aqui
            bank[pack].idealTimeArraySize = int(idealTimeArraySize/(highestFreq/bank[pack].Fs))
            bank[i].data = -20000*np.ones(bank[pack].idealTimeArraySize)
        print(bank[pack].idealTimeArraySize)

    # Cria vetores com valores de tempo, em segundos
    for pack in receivedPacks:
        bank[pack].createTimeVector(firstTimeVal, idealTimeArraySize, highestFreq)
        # print(bank[entry].time)
        print(len(bank[pack].time))

    bank['time'] = bank[highFreqPack].time

    # Monta vetores novos do pacote 1 e 2 no tempo ideal nas posições
    # correspondentes. Caso não haja perda de pacotes, o resultado é um vetor
    # igual ao original.
    # Caso haja perda, as posições nas quais houveram perdas manterão o valor
    # de -200
    for pack in receivedPacks:
        for i in range(indexFirstElement[pack-1], indexFirstElement[pack-1] + bank[pack].idealTimeArraySize):
            if len(bank[pack].packData) != 0:
                # Caso chegou no fim do array antes de chegar em idealTimeArraySize
                if i == len(bank[pack].packData[-1]):
                    break
                delta = (bank[pack].packData[-1][i] - firstTimeVal)/(highestFreq/bank[pack].Fs)
                delta = int(delta)
                if delta >= bank[pack].idealTimeArraySize:
                    break
                pack1list = bank[pack].dataOrder
                for entry in pack1list:
                    currentData = bank[entry]
                    currentData.data[delta] = bank[pack].packData[currentData.positionInPack][i]


    #plt.plot(bank[2].time, bank['rpm'].data)


    # Interpola se achar -20000
    for pack in receivedPacks:
        if bank[pack].loss != 1:
            for dta in bank[pack].dataOrder:
                bank[dta] = linearInterp(bank[dta], -20000, bank[pack].idealTimeArraySize)


    # Interpola para colocar todos os dados na mesma base de tempo
    for pack in receivedPacks:
        if len(bank[pack].packData) != 0:
            if bank[pack].Fs != highestFreq:
                pack2list = bank[pack].dataOrder
                for entry in pack2list:
                    currentData = bank[entry]
                    currentData.data = np.interp(bank['time'], bank[pack].time, currentData.data)


    # Aplica funcoes
    if ui.radioButton.isChecked():
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



# Roda janela

if __name__ == "__main__":
    import sys

    app = 0
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #app.exec_()

    ui.actionOpenFile.triggered.connect(selectFile)
    ui.actionTitulo.triggered.connect(plotSetTitle)
    ui.actionEixo_X.triggered.connect(plotSetX)
    ui.actionEixo_Y.triggered.connect(plotSetY)
    ui.actionExportar_para_CSV.triggered.connect(exportToCSV)
    ui.listWidget.itemDoubleClicked.connect(listClicked)
    ui.clearPlotButton.clicked.connect(clearPlots)  # botão para atualizar as portas seriis disponíveis
    ui.resetButton.clicked.connect(resetMultOffset)
    #sys.exit(app.exec_())



sys.exit(app.exec_())
