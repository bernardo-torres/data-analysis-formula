import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import easygui
from defines import*

dictTeste = {}
pacotes = {}
pacote1 = []
pacote2 = []
pacote3 = []
pacote4 = []
data = []
EXT_DATA_STATUS = 0
NPACK = 0
Fs = 40
Fs2 = Fs/2
Fs3 = Fs/20
T = 1/Fs
T2 = 1/Fs2
T3 = 1/Fs3

print('a')
# Abre arquivo
file_path = r'C:\Users\befto\Dropbox\Python\SkidPad_11_9__Pedico_2.txt'
# file_path = easygui.fileopenbox()
with open(file_path) as file_object:m
    # Salva arquivo na lista lines
    lines = file_object.readlines()
for line in lines:
    # Ignora linhas vazias
    if line != '\n':
        # Remove \n
        currentLine = line.strip()
        splitLine = currentLine.split()
        # Pega ordem dos dados do campo DADOS e armazena em dicionario
        if currentLine[0:6] == 'DADOSP':
            packNo = currentLine[6]
            for index, x in enumerate(splitLine, start=1):
                # Adiciona entradas correspondentes aos dados
                dictTeste[x] = dataType(packNo, index-1, 0, Fs)
                # Adiciona entrada DADOSPX contendo a linha com a informacao dos dados
                dictTeste[splitLine[0]] = splitLine[1:-1]
            NPACK = int(packNo)
        # Analisa linha por linha e divide conforme pacotes
        # Caso o primeiro caractere da linha seja um decimal
        if currentLine[0].isdecimal() == 1:
            # Pega o valor do primeiro caractere (ideitificador do pacote)
            if currentLine[0] == '1':
                # Separa linha por palavra e converte para int. Adiciona a lista pacote1
                aux = [int(x) for x in splitLine[1: len(splitLine)]]
                pacote1.append(aux)
            elif currentLine[0] == '2':
                aux = [int(x) for x in splitLine[1:len(splitLine)]]
                pacote2.append(aux)
            elif currentLine[0] == '3':
                aux = [int(x) for x in splitLine[1:len(splitLine)]]
                pacote3.append(aux)
            elif currentLine[0] == '4':
                aux = [int(x) for x in splitLine[1:len(splitLine)]]
                pacote4.append(aux)

pack1 = np.array(pacote1)
pack1 = pack1.T
pack2 = np.array(pacote2)
pack2 = pack2.T
pack3 = np.array(pacote3)
pack3 = pack3.T
# Caso tenha recebido dados do pacote 4
if len(pacote4) != 0:
    EXT_DATA_STATUS = 1
    pack4 = np.array(pacote1)
    pack4 = pack4.T

lastTimeVal = pack1[-1][-1]
firstTimeVal = pack1[-1][0]
lastTimeValP3 = pack3[-1][-1]
firstTimeValP3 = pack3[-1][0]
elapsedTime = (lastTimeVal-firstTimeVal)/Fs
idealTimeArraySize = lastTimeVal-firstTimeVal + 1
elapsedTimeP2 = (pack2[-1][-1]-pack2[-1][0])/Fs
elapsedTimeP3 = (lastTimeValP3-firstTimeValP3)/Fs

# Tamanho dos vetores do pacote 1 e calcula perda percentual de pacotes
sizeP1 = (pack1[-1]).size
packetLoss = (sizeP1)/idealTimeArraySize
print('Packetloss = '+ str(packetLoss))

# Usa pacote 3 para definir o tamanho de um vetor de dados perfeito (sem perdas)
idealTimeArraySize = lastTimeValP3-firstTimeValP3+1
if (idealTimeArraySize % 2) == 1:
    idealTimeArraySize -= 1
idealTimeArraySize2 = int(idealTimeArraySize/(Fs/Fs2))
idealTimeArraySize3 = int(idealTimeArraySize/(Fs/Fs3))


# Acha em qual posição do vetor de tempo do pacote 1 esta o primeiro valor de
# tempo do pacote 3
indexFirstElementP1 = list(pack1[-1]).index(firstTimeValP3)
indexFirstElementP2 = list(pack2[-1]).index(firstTimeValP3)

# Cria vetores inicializados com -20000
for entry in dictTeste['DADOSP1']:
    dictTeste[entry].data = -20000*np.ones(idealTimeArraySize)
for entry in dictTeste['DADOSP2']:
    dictTeste[entry].data = -20000*np.ones(idealTimeArraySize2)
for entry in dictTeste['DADOSP3']:
    dictTeste[entry].data = -20000*np.ones(idealTimeArraySize3)


# Cria vetores com valores de tempo, em segundos
time = np.arange(firstTimeValP3*T, lastTimeValP3*T, T)
dictTeste['time'] = time
time2 = np.arange(firstTimeValP3*T, lastTimeValP3*T, T2)
time3 = np.arange(firstTimeValP3*T, lastTimeValP3*T, T3)

# Monta vetores novos do pacote 1 e 2 no tempo ideal nas posições
# correspondentes. Caso não haja perda de pacotes, o resultado é um vetor
# igual ao original.
# Caso haja perda, as posições nas quais houveram perdas manterão o valor
# de -200
for i in range(indexFirstElementP1,indexFirstElementP1 + idealTimeArraySize):
    # Caso chegou no fim do array antes de chegar em idealTimeArraySize
    delta = pack1[-1][i] - firstTimeValP3
    if delta == idealTimeArraySize:
        break
    pack1list = dictTeste['DADOSP1']
    for entry in pack1list:
        currentData = dictTeste[entry]
        currentData.data[delta] = pack1[currentData.positionInPack-1][i]
for i in range(indexFirstElementP2, indexFirstElementP2 + int(idealTimeArraySize2)):
    # Caso chegou no fim do array antes de chegar em idealTimeArraySize
    delta = int((pack2[-1][i] - firstTimeValP3)/(Fs/Fs2))
    if delta == idealTimeArraySize2:
        break
    pack2list = dictTeste['DADOSP2']
    for entry in pack2list:
        currentData = dictTeste[entry]
        currentData.data[delta] = pack2[currentData.positionInPack-1][i]
for i in range(0, int(idealTimeArraySize3)):
    # Caso chegou no fim do array antes de chegar em idealTimeArraySize
    delta = int((pack3[-1][i] - firstTimeValP3)/(Fs/Fs3))
    if delta == idealTimeArraySize3:
        break
    pack3list = dictTeste['DADOSP3']
    for entry in pack3list:
        currentData = dictTeste[entry]
        currentData.data[delta] = pack3[currentData.positionInPack-1][i]

# Interpola se achar -20000, a vir

a = dictTeste['rearBrakeP'].data
pack2list = dictTeste['DADOSP2']
for entry in pack2list:
    currentData = dictTeste[entry]
    currentData.data = np.interp(time, time2, currentData.data)


print(len(dictTeste['velDD'].data), len(dictTeste['rearBrakeP'].data), len(dictTeste['ect'].data))

x = np.arange(0,idealTimeArraySize3,1)
xvals = np.arange(0,idealTimeArraySize,1)
yinterp = np.interp(time, time3,dictTeste['ect'].data)

plt.plot(time3, dictTeste['ect'].data)
plt.plot(time, yinterp, time, dictTeste['rearBrakeP'].data)
plt.plot(time2,a)
plt.show()
print(dictTeste['DADOSP2'])


print(xvals,x, len(dictTeste['ect'].data))
