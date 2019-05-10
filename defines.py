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

    def calcTimeArraySize(self, highestFreq):
        a = self.packData[-1][-1] - self.packData[-1][0] + 1
        self.idealTimeArraySize = int(a/(highestFreq/self.Fs))
        return a

    def createTimeVector(self, first, last, highestFreq):
        T = 1/highestFreq
        self.time = np.arange(first*T, last*T, 1/(self.Fs))
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
    'velDD': [mult, 1, 0],
    'velT': [mult, 1, 0],
    'sparkCut': [mult, 1, 0],
    'suspPos': [lin, suspMAX, suspMIN, 240, 120],
    'oleoP': [mult, 0.001, 0],
    'fuelP': [mult, 0.001, 0],
    'tps': [mult, 0.1, 0],
    'rearBrakeP': [mult, 0.02535, 5.2],
    'frontBrakeP': [mult, 0.02535, 5.9],
    'volPos': [lin, volMAX, volMIN, -240, 120],
    'beacon': [mult, 1, 0],
    'correnteBat': [mult, 0.014652, 29.3],
    'ect': [mult, 0.1, 0],
    'batVoltage': [mult, 0.01, 0],
    'releBomba': [mult, 1, 0],
    'releVent': [mult, 1, 0],
    'pduTemp': [mult, 1, 0],
    'tempDiscoD': [mult, 1, 0],
    'tempDiscoE': [mult, 1, 0]
}

baseString = 'ind acelX acelY acelZ velDD velT sparkCut suspPos time'
baseString += ' oleoP fuelP tps rearBrakeP frontBrakeP volPos beacon correnteBat'
baseString += ' ect batVoltage releBomba releVent pduTemp tempDiscoD tempDiscoE'

filter = [-0.000182237767686131, -0.00019443361140151, -2.20485262156374, 0.00199733368612105	,0.00215815350457003,	1.77586707895554e-06,	-0.0108808297302813,	-0.0119995093390945,	-6.77990530852142e-06,	0.0400087812172113,	0.0458068917029619,	1.61071326654185e-05,	-0.118676546839361,	-0.148505247416218,	-2.63186020677598e-05,	0.400060614488955,	0.800407026948887	,1.00003087829646,	0.800407026948887,	0.400060614488955,	-2.63186020677598e-05,	-0.148505247416218,	-0.118676546839361,	1.61071326654185e-05,	0.0458068917029619,	0.0400087812172113,	-6.77990530852142e-06,	-0.0119995093390945,	-0.0108808297302813,	1.77586707895554e-06,	0.00215815350457003,	0.00199733368612105,	-2.20485262156374e-07,	-0.000194433611401518,	-0.000182237767686131]
print(filter)
