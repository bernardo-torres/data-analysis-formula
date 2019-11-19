import numpy as np

volMAX = 3770
volMIN = 345
suspMAX = 4000
suspMIN = 0


class dataType():
    def __init__(self, packNo, positionInPack, data, Fs):
        self.positionInPack = positionInPack
        self.packNo = packNo
        self.data = data
        self.Fs = Fs


class pacotes():
    def __init__(self, packNo, dataOrder, Fs):
        self.packNo = packNo
        self.dataOrder = dataOrder
        self.Fs = Fs
        self.packData = []
        self.idealTimeArraySize = 0
        self.time = 0
        self.loss = 0

    def calcTimeArraySize(self, highestFreq):
        a = self.packData[-1][-1] - self.packData[-1][0]
        self.idealTimeArraySize = int(a/(highestFreq/self.Fs)) + 1
        return a

    def createTimeVector(self, first, arraySize, highestFreq):
        T = 1/highestFreq
        self.time = np.arange(0, self.idealTimeArraySize)/(self.Fs) + first*T
        #.arange(first*T, (first+arraySize)*T, 1/(self.Fs))
        return self.time


def mult(array, value, offset):
    return (array*value - offset)


def lin(array, MAX, MIN, range, offset):
    auxx = (array - MAX)*range/(MAX-MIN) - offset
    return auxx


dic1 = {
    'acelX': [mult, -1/16384, 0],
    'acelY': [mult, 1/16384, 0],
    'acelZ': [mult, 1/16384, 0],
    'velT': [mult, 1, 0],
    'sparkCut': [mult, 1, 0],
    'suspPos': [lin, suspMAX, suspMIN, 240, 120],
    'oleoP': [mult, 0.001, 0],
    'fuelP': [mult, 0.001, 0],
    'tps': [mult, 0.1, 0],
    'rearBrakeP': [mult, 0.02535, 5.2],
    'frontBrakeP': [mult, 0.02535, 5.9],
    'volPos': [lin, volMIN, volMAX, -240, 120],
    'beacon': [mult, 1, 0],
    'correnteBat': [mult, 0.014652, 29.3],
    'ect': [mult, 0.1, 0],
    'batVoltage': [mult, 0.01, 0],
    'releBomba': [mult, 1, 0],
    'releVent': [mult, 1, 0],
    'pduTemp': [mult, 1, 0],
    'tempDiscoD': [mult, 1, 0],
    'tempDiscoE': [mult, 1, 0],
    'ext1': [mult, 1, 0], 'ext2': [mult, 1, 0], 'ext3': [mult, 1, 0], 'ext4': [mult, 1, 0], 'ext5': [mult, 1, 0],
    'ext6': [mult, 1, 0], 'ext7': [mult, 1, 0], 'ext8': [mult, 1, 0], 'ext9': [mult, 1, 0], 'ext10': [mult, 1, 0],
    'ext11': [mult, 1, 0], 'ext12': [mult, 1, 0],

    'acelX_DD': [mult, 1/16384, 0], 'acelY_DD': [mult, 1/16384, 0], 'acelZ_DD': [mult, 1/16384, 0],
    'acelX_DE': [mult, 1/16384, 0], 'acelY_DE': [mult, 1/16384, 0], 'acelZ_DE': [mult, 1/16384, 0],
    'acelX_TD': [mult, 1/16384, 0], 'acelY_TD': [mult, 1/16384, 0], 'acelZ_TD': [mult, 1/16384, 0],
    'acelX_TE': [mult, 1/16384, 0], 'acelY_TE': [mult, 1/16384, 0], 'acelZ_TE': [mult, 1/16384, 0],
    'velDD': [mult, 1, 0], 'velDE': [mult, 1, 0], 'velTD': [mult, 1, 0], 'velTE': [mult, 1, 0],
    'rpm': [mult, 1, 0],
    'injectors': [mult, 1, 0],
    'suspDE': [mult, 1, 0], 'suspDD': [mult, 1, 0], 'suspTE': [mult, 1, 0], 'suspTD': [mult, 1, 0],
    'correnteVent': [mult, 1, 0], 'correnteBomba': [mult, 1, 0],
    'oilTemp': [mult, 1, 0], 'tempDiscoDE': [mult, 1, 0], 'tempDiscoDD': [mult, 1, 0],
    'tempDiscoTE': [mult, 1, 0], 'tempDiscoTD': [mult, 1, 0],
    'tempVent': [mult, 1, 0], 'tempBomba': [mult, 1, 0], 'runners': [mult, 1, 0],
    'mata': [mult, 1, 0], 'gpsLat': [mult, 1, 0], 'gpsLong': [mult, 1, 0],
    'gpsNS': [mult, 1, 0], 'gpsEW': [mult, 1, 0]
}


# Funcao que interpola linearmente um array entre dois pontos
def linearInterp(vector, value, size):
    cnt = 0
    for i in range(0, size):
        if vector.data[i] == value:
            cnt = cnt + 1
        elif cnt != 0:
            delta = vector.data[i] - vector.data[i-cnt-1]
            dv = delta/(cnt+1)
            k = 1
            for j in range(i-cnt, i):
                vector.data[j] = vector.data[i-cnt-1] + dv*k
                k = k + 1
            cnt = 0
    return vector

# Só para teste
baseString = 'ind acelX acelY acelZ velDD velT sparkCut suspPos time'
baseString += ' oleoP fuelP tps rearBrakeP frontBrakeP volPos beacon correnteBat'
baseString += ' ect batVoltage releBomba releVent pduTemp tempDiscoD tempDiscoE'

print('Versão atual ----  1.0 ---- 09/09/19')
print('Ultimas Mudancas:')
print('beta 0.2 -- 31/05')
print('Clique no grafico para exibir os valores de um ponto especifico')
print('Para retirar esse marcador, clique em cima com botao direito')
print('Agora interpolando perda de pacotes')
print('Pegando max e min da posicao do volante por meio do txt')
print('Nova interface')
print('beta 0.3')
print('Possivel adicionar multiplier e offset com decimais (utiliza-de . e nao ,)')
print('Pegando max e min da posicao da suspensao por meio do txt')
print('1.0')
print('Nova interface usando Pyqt5')
