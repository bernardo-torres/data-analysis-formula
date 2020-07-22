
# Modulos
import matplotlib.pyplot as plt
import sys
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import pandas as pd
from scipy.signal import savgol_filter


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
    data = df[item.text()].values * mult + offset

    if ui.hampelActive.isChecked():
        name = name+'_h'
    if ui.savgol.isChecked():
        name = name+'_s'

    if name in dataDictionary:
        #dataDictionary[name].remove()
        del dataDictionary[name]
    else:
        if ui.hampelActive.isChecked():
            window = int(ui.multiplierLineEdit_2.text())
            t0 = int(ui.offsetLineEdit_2.text())
            data= hampel(pd.Series(data),window, t0)
            data = data.values

        if ui.savgol.isChecked():
            window = int(ui.multiplierLineEdit_3.text())
            order = int(ui.offsetLineEdit_3.text())
            data = savgol_filter(data, window, order)


        dataDictionary[name] = data

    ui.widget.mplPlot(bank['time'],data, name)
    print(item.text())



def clearPlots():
    ui.widget.mplClear()
    dataDictionary.clear()


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
    text = showDialog()
    ui.widget.mplSetXLabel(text)




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


def exportProTune():
    global bank, dataDictionary, df
    fileName, _ = QtWidgets.QFileDialog.getSaveFileName(MainWindow, "Escolha pasta e nome do arquivo dlf",
                                                        "", 'dlf(*.dlf)')
    dataNames = ""
    for name in df.columns:
        dataNames = dataNames + name + ";"

    units="seg.;"
    for name in df.columns:
        units = units + dic1[name][-1] + ";"

    text = ("#V2\n"
    "#DATASTART\n"
    "Datalog Time;") + dataNames + "\n" + units + "\n"
    print(text)
    df2 = df.copy()
    df2.index = bank['time']
    dataText = df2.to_csv(header=False, sep="A")
    #dataText = dataText.replace("  ", "A")
#    dataText = dataText.replace(" ", "A")

    text = text+dataText
    print(fileName)
    with open(fileName, "w") as text_file:
        text_file.write(text)


def displayErrorMessage(text):
    dlg = QtWidgets.QMessageBox(None)
    dlg.setWindowTitle("Error!")
    dlg.setIcon(QtWidgets.QMessageBox.Warning)
    dlg.setText(
     "<center>" + text + "<center>")
    dlg.exec_()
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
daf = ['a', 'b', 'c'] # remover
df = pd.DataFrame()



def runAnalysis(file_path):
    try:
        global highFreqPack, NPACK, bank, dataDictionary, df, daf
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
                    try:
                        Fs = float(splitLine[1])
                    except Exception as ex:
                        print(len(ex.args))
                        print(ex.args)
                        print("Não conseguiu rodar analise, problema nas taxas de amostragem dos pacotes")
                        displayErrorMessage('Não conseguiu rodar analise, problema nas taxas de amostragem dos pacotes')

                    dataOrder = splitLine[2:-1]
                    # Adiciona entrada DADOSPX no dicionario
                    # contendo a linha com a informacao dos dados
                    # ex bank[DADOSP2] = [oleoP fuelP...]
                    bank[packNo] = pacotes(packNo, dataOrder, Fs)
                    for index, x in enumerate(dataOrder, start=0):
                        # Adiciona entradas correspondentes aos dados
                        #print(x, index)
                        print("Pacote: "+str(packNo)+". Dado: "+x+". Indice: "+str(index))
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
                        displayErrorMessage("TXT nao possui formado esperado, inserir linhas descrevendo a ordem dos dados nos pacotes")
                        #print("TXT nao possui formado esperado")
                        return
                    # Pega o valor do primeiro caractere (ideitificador do pacote)
                    currentPackNo = int(currentLine[0])
                    # Medida para evitar erros, caso o identificador venha errado
                    if currentPackNo in receivedPacks:
                        # Converte dados separados em splitLine para inteiros
                        try:
                            aux = [float(x) for x in splitLine[1: len(splitLine)]]
                            # Adiciona lista com valores da linha

                            if len(bank[currentPackNo].dataOrder)+1 == len(aux):
                                bank[currentPackNo].packData.append(aux)
                        except :
                            print('Problema na leitura da linha : '+currentLine)


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


        # Verifica se em algum momento o tempo foi resetado

        for pack in receivedPacks:
            rowsToRemove = []
            if len(bank[pack].packData) != 0:
                lastTime = bank[pack].packData[-1][0]
                resetCount = 0
                for time, i in zip(bank[pack].packData[-1], range(0, len(bank[pack].packData[-1]))):
                    if time < lastTime:
                        if lastTime < bank[pack].packData[-1][i+1]:
                            print('Problema no pacote '+ str(pack) + ' no valor de tempo ' + str(time))
                            rowsToRemove.append(i)
                            time = lastTime + int(highestFreq/bank[pack].Fs)
                        elif bank[pack].packData[-1][i] > bank[pack].packData[-1][i-2]:
                            print('Problema (outlier) no pacote '+ str(pack) + ' no valor de tempo ' + str(lastTime))
                            rowsToRemove.append(i-1)
                            #time = lastTime + int(highestFreq/bank[pack].Fs)
                        else:
                            resetCount = resetCount+1
                    lastTime = time
                    time = time + resetCount*65536
                    bank[pack].packData[-1][i] = time
            if len(rowsToRemove)>0:
                bank[pack].packData = np.delete(bank[pack].packData, rowsToRemove, 1)

        # Remove do dicionario dados que foram anunciados no txt mas nao apareceram nos dados
        for pack in receivedPacks:
            if len(bank[pack].packData) == 0:
                [bank.pop(a) for a in bank[pack].dataOrder]


        columns = [data for pack in receivedPacks for data in bank[pack].dataOrder ]

    #    import time as tim
    #    start_time = tim.time()


        # Cria dataframe com dados dos pacotes e concatena os dataframes de pacotes diferentes
        init=False
        for pack in receivedPacks:
            if len(bank[pack].packData) != 0:
                dat = pd.DataFrame(data=bank[pack].packData.T)
                dat = dat.set_index(dat.columns[-1])
                dat.columns = bank[pack].dataOrder
                dat = dat.groupby(dat.index).first()
                bank[pack].loss = len(dat.index) # Inicialmente loss contem o numero de pontos recebidos, para de cada pacote
                if init==False:
                    init=True
                    df = dat.copy()
                else:
                    df = pd.concat([df, dat], axis=1, sort=False).copy()



        # Subtrai de todos os indices o valor do indice 0
        df.index = df.index - df.index[0]

    #    daf[0] = df.copy()

    #    print("--- %s seconds ---" % (tim.time() - start_time))


        # Aplica funcoes
        if ui.radioButton.isChecked():
            for i in dic1:
                aux = bank.get(i, KEY_NOT_FOUND)
                if aux != KEY_NOT_FOUND:
                    print(i)
                    if dic1[i][0] == mult:
                        df[i] = dic1[i][0](df[i].values, dic1[i][1], dic1[i][2])
                    else:
                        df[i] = dic1[i][0](df[i].values, dic1[i][1], dic1[i][2], dic1[i][3], dic1[i][4])

    #    daf[1]= df.copy()

        # Reindex coloca nulos nos indices faltantes
        df = df.reindex(np.arange(0, df.index[-1]+1))

    #    daf[2] = df.copy()

        # Converte para numeric
        for col in df:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        offset = 0
        multiplier = 1

        # Adiciona itens na lista da interface
        for i in dic1:
            aux = bank.get(i, KEY_NOT_FOUND)
            if aux != KEY_NOT_FOUND:
                ui.listWidget.addItem(i)

        # Calcula perda e dispoe na interface
        for pack in receivedPacks:
            if len(bank[pack].packData) != 0:
                print(bank[pack].loss, len(df.index))
                bank[pack].loss = bank[pack].loss/len(df.index)
                bank[pack].loss = bank[pack].loss * highestFreq/bank[pack].Fs
        if 1 in bank:
            ui.label_6.setText("Pacote 1: " + str(round(bank[1].loss*100,2)) + '%')
        if 2 in bank:
            ui.label_7.setText("Pacote 2: " + str(round(bank[2].loss*100,2)) + '%')
        if 3 in bank:
            ui.label_8.setText("Pacote 3: " + str(round(bank[3].loss*100,2)) + '%')
        if 4 in bank:
            ui.label_10.setText("Pacote 4: " + str(round(bank[4].loss*100,2)) + '%')

        # Interpola
        df = df.interpolate(limit_direction='both')

        # Vetor de tempo
        bank['time'] = df.index/highestFreq

        ui.label_4.setText("Numero de pontos: " + str(len(df.index)))
        ui.widget.mplSetXLabel('Tempo(s)')


    except Exception as ex:
        print(len(ex.args))
        print(ex.args)
        print("Não conseguiu rodar analise")
        displayErrorMessage('Não conseguiu rodar analise')




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
#    app.exec_()

    ui.actionOpenFile.triggered.connect(selectFile)
    ui.actionTitulo.triggered.connect(plotSetTitle)
    ui.actionEixo_X.triggered.connect(plotSetX)
    ui.actionEixo_Y.triggered.connect(plotSetY)
    ui.actionExportar_para_CSV.triggered.connect(exportToCSV)
    ui.actionExportar_Txt_Pro_Tune.triggered.connect(exportProTune)
    ui.listWidget.itemDoubleClicked.connect(listClicked)
    ui.clearPlotButton.clicked.connect(clearPlots)  # botão para atualizar as portas seriis disponíveis
    ui.resetButton.clicked.connect(resetMultOffset)
    sys.exit(app.exec_())



#sys.exit(app.exec_())
