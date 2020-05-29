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
            if i == (size-1):
                for j in range(i-cnt, i+1):
                    vector.data[j] = vector.data[i-cnt]
        elif cnt != 0:
            delta = vector.data[i] - vector.data[i-cnt-1]
            dv = delta/(cnt+1)
            k = 1
            for j in range(i-cnt, i):
                vector.data[j] = vector.data[i-cnt-1] + dv*k
                k = k + 1
            cnt = 0


    return vector


def hampel(vals_orig, k=7, t0=3):
    '''
    vals: pandas series of values from which to remove outliers
    k: size of window (including the sample; 7 is equal to 3 on either side of value)
    '''

    #Make copy so original not edited
    vals = vals_orig.copy()

    #Hampel Filter
    L = 1.4826
    rolling_median = vals.rolling(window=k, center=True).median()
    MAD = lambda x: np.median(np.abs(x - np.median(x)))
    rolling_MAD = vals.rolling(window=k, center=True).apply(MAD)
    threshold = t0 * L * rolling_MAD
    difference = np.abs(vals - rolling_median)

    '''
    Perhaps a condition should be added here in the case that the threshold value
    is 0.0; maybe do not mark as outlier. MAD may be 0.0 without the original values
    being equal. See differences between MAD vs SDV.
    '''

    outlier_idx = difference > threshold
#    vals[outlier_idx] = np.nan
    vals[outlier_idx] = rolling_median[outlier_idx]
    return(vals)

#def hampel(x,k,method="center",thr=3):
#    #Input
#    # x       input data
#    # k       half window size (full 2*k+1)
#    # mode    about both ends
#    #         str {‘center’, 'same','ignore',‘nan’}, optional
#    #
#    #           center  set center of window at target value
#    #           same    always same window size
#    #           ignore  set original data
#    #           nan     set non
#    #
#    # thr     threshold (defaut 3), optional
#    #Output
#    # newX    filtered data
#    # omadIdx indices of outliers
#    arraySize=len(x)
#    idx=np.arange(arraySize)
#    newX=x.copy().values
#    omadIdx=np.zeros_like(x)
#    for i in range(arraySize):
#        mask1=np.where( idx>= (idx[i]-k) ,True, False)
#        mask2=np.where( idx<= (idx[i]+k) ,True, False)
#        kernel= np.logical_and(mask1,mask2)
#        if method=="same":
#            if i<(k):
#                kernel=np.zeros_like(x).astype(bool)
#                kernel[:(2*k+1)]=True
#            elif i>= (len(x)-k):
#                kernel=np.zeros_like(x).astype(bool)
#                kernel[-(2*k+1):]=True
#        #print (kernel.astype(int))
#        #print (x[kernel])
#        med0=np.median(x[kernel])
#        #print (med0)
#        s0=1.4826*np.median(np.abs(x[kernel]-med0))
#        if np.abs(x[i]-med0)>thr*s0:
#             omadIdx[i]=1
#             newX[i]=med0
#
#    if method=="nan":
#        newX[:k]=np.nan
#        newX[-k:]=np.nan
#        omadIdx[:k]=0
#        omadIdx[-k:]=0
#    elif method=="ignore":
#        newX[:k]=x[:k]
#        newX[-k:]=x[-k:]
#        omadIdx[:k]=0
#        omadIdx[-k:]=0
#
#    return newX,omadIdx.astype(bool)
#


# Só para teste
baseString = 'ind acelX acelY acelZ velDD velT sparkCut suspPos time'
baseString += ' oleoP fuelP tps rearBrakeP frontBrakeP volPos beacon correnteBat'
baseString += ' ect batVoltage releBomba releVent pduTemp tempDiscoD tempDiscoE'

print('Versão atual ----  1.1 ---- 11/19')
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
print('1.1')
print('Conserto de bugs, exportar para csv')
print('2.0')
print('Uso mais extenso do pandas')

print('Abrindo arquivo functions.txt')
try:
    with open('functions.txt', 'r') as document:
        dic1 = {}
        for line in document:
            line = line.split()
            if not line:  # empty line?
                continue
            for i in range(2, len(line)):
                line[i] = float(line[i])
            if line[1] == 'mult':
                line[1] = mult
            elif line[1] == 'lin':
                line[1] = lin
            dic1[line[0]] = line[1:]
except:
    print('Falha ao abrir functions.txt')
