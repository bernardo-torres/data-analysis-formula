
import matplotlib.pyplot as plt
from scipy import signal
import easygui
from defines import*
from matplotlib import interactive
interactive(True)
from mpldatacursor import datacursor


bank = {}
EXT_DATA_STATUS = 0
KEY_NOT_FOUND = -1
NPACK = 0
DELIMITER = ' '
Fs = 40
Fs2 = Fs/2
Fs3 = Fs/20
T = 1/Fs
T2 = 1/Fs2
T3 = 1/Fs3

# Abre arquivo
file_path = r'C:\Users\befto\Dropbox\Python\SkidPad_11_9__Pedico_2.txt'
file_path = easygui.fileopenbox()
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
        # Analisa linha por linha e divide conforme pacotes
        # Caso o primeiro caractere da linha seja um decimal
        if currentLine[0].isdecimal() == 1:
            # Pega o valor do primeiro caractere (ideitificador do pacote)
            currentPackNo = int(currentLine[0])
            # Medida para evitar erros, caso o identificador venha errado
            if currentPackNo <= NPACK:
                # Converte dados separados em splitLine para inteiros
                aux = [int(x) for x in splitLine[1: len(splitLine)]]
                # Adiciona lista com valores da linha
                bank[currentPackNo].packData.append(aux)


lowFreqPack = 0
highFreqPack = 0
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
        indexFirstElement[entry-1] = np.where(bank[entry].packData[-1] == firstTimeVal)[0][0]
        # print(indexFirstElement)

indexFirstElement = indexFirstElement.astype(int)

packetLoss = len(bank[highFreqPack].packData[-1])/(bank[highFreqPack].idealTimeArraySize)
print('Packetloss = ' + str(packetLoss))

# Calcula tamanho ideal para os vetores
idealTimeArraySize = bank[lowFreqPack].idealTimeArraySize*highestFreq/lowestFreq
if (idealTimeArraySize % 2) == 1:
    idealTimeArraySize -= 1
print('Tamanho do vetor ideal = ' + str(idealTimeArraySize))

# Cria vetores inicializados com -20000
for entry in range(1, NPACK+1):
    for i in bank[entry].dataOrder:
        # ver isso aqui
        bank[entry].idealTimeArraySize = int(idealTimeArraySize/(highestFreq/bank[entry].Fs))
        bank[i].data = -20000*np.ones(bank[entry].idealTimeArraySize)

# Cria vetores com valores de tempo, em segundos
for entry in range(1, NPACK+1):
    bank[entry].createTimeVector(firstTimeVal, lastTimeVal, highestFreq)
    # print(bank[entry].time)

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
            delta = (bank[j].packData[-1][i] - firstTimeVal)/(highestFreq/bank[j].Fs)
            delta = int(delta)
            if delta == bank[j].idealTimeArraySize:
                break
            pack1list = bank[j].dataOrder
            for entry in pack1list:
                currentData = bank[entry]
                currentData.data[delta] = bank[j].packData[currentData.positionInPack][i]


#plt.plot(bank[3].time, bank['ect'].data)


# Interpola se achar -20000
if packetLoss < 1:
    for entry in range(1, NPACK+1):
        for dta in bank[entry].dataOrder:
            bank[dta] = linearInterp(bank[dta], -20000, bank[entry].idealTimeArraySize)

#plt.plot(bank[3].time, bank['ect'].data)
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

print('Entre com o dado para ser plotado')
x = input()
while x != 'end':

    offset = 0
    multiplier = 1
    splitLine = x.split()
    aux = bank.get(splitLine[0], KEY_NOT_FOUND)
    if aux != KEY_NOT_FOUND:
        if len(splitLine) == 2:
            multiplier = float(splitLine[1])
        elif len(splitLine) == 3:
            offset = float(splitLine[2])
        plt.plot(bank['time'], bank[splitLine[0]].data*multiplier+offset, linewidth=0.5)
        plt.xlabel('Tempo (s)')
        datacursor(bbox=None, draggable=True, display='multiple')
    elif x == 'figure':
        plt.figure()
    else:
        print('Dado nao existente')

    print('Entre com o dado para ser plotado. Digite figure para abrir uma figura nova. End para encerrar.')
    x = input()



#plt.plot(bank['time'], bank['ect'].data)
#plt.show()
