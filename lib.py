import random
import numpy as np

class individual:
    def __init__(self, x="111111111111111", y="111111111111111"):
        self.realX = random.randint(-10000, 10000)%1000
        self.realY = random.randint(-10000, 10000)%1000
        self.binX = realToBinary(self.realX)
        self.binY = realToBinary(self.realY)
        self.fitness = fit_func(self.realX, self.realY)


def fit_func(x, y):
    return -(np.power(x, 2) + np.power(y, 2)) + 4

def binaryToReal(binNum):
    signalBit = binNum[0]
    realNum = int(binNum[1:], 2)*0.001
    
    return -realNum if signalBit == '1' else realNum

def realToBinary(realNum):
    realNum = realNum*1000
    if realNum < 0:
        signalBit = '1'
    else:
        signalBit = '0'

    binaryNum = bin(int(abs(realNum)))
    print(binaryNum)
    binaryNum = binaryNum[2:]
    binaryNum = "0"*(14-len(binaryNum))+binaryNum

    return signalBit+binaryNum

def tournamentSel(population, sampleSize):
    sample = random.sample(population, sampleSize)

