import random
import numpy as np
import matplotlib.pyplot as plt

class individual:
    def __init__(self, x, y):
        self.real_x = x
        self.real_y = y
        self.bin_x = realToBinary(x)
        self.bin_y = realToBinary(y)
        self.fit = fitFunc(self.real_x, self.real_y)

class population:
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.generation = 1
        self.individuals = self.initFirstGen()
    
    def initFirstGen(self):
        pop = []
        for i in range(self.pop_size):
            pop.append(individual(random.randint(-10000, 10000)/1000, random.randint(-10000, 10000)/1000))
            #print(pop[i].real_x, pop[i].real_y, pop[i].fit)
        return pop
    
    def plotGraph(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = []
        y = []
        z = []

        for individual in self.individuals:
            x.append(individual.real_x)
            y.append(individual.real_y)
        z = fitFunc(x, y)

        ax.scatter(x, y, z, color='red', s=10, label='Points')

        ax.set_xlabel('Gene X')
        ax.set_ylabel('Gene Y')
        ax.set_zlabel('Fitness')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_zlim(-200, 10)
        title = str(self.generation)+"° Geração"
        ax.set_title(title)

        ax.legend()

        filename = "./graficos/gen"+str(self.generation)+".png"
        plt.savefig(filename)


def fitFunc(x, y):
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
    binaryNum = binaryNum[2:]
    binaryNum = "0"*(14-len(binaryNum))+binaryNum

    return signalBit+binaryNum

a = population(10)
a.plotGraph()