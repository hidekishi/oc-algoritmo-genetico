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
    def __init__(self, pop_size, cross_rate, mutation_rate):
        self.pop_size = pop_size
        self.generation = 1
        self.mutation_rate = mutation_rate*100 # Para realizar operacoes com inteiros ao inves de float
        self.cross_rate = cross_rate*100       # Idem
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

    def cross(self, par_1_index, par_2_index):

        def bound_check(bin_gene):
            real_gene = binaryToReal(bin_gene)
            if real_gene >= -10 and real_gene <= 10:
                return True
            return False
        
        def mutation(original_gene, mut_rate):
            mut_gene = []
            for bit in original_gene:
                if random.randint(0, 100) < mut_rate:
                    if bit == "1":
                        mut_gene.append("0")
                    else:
                        mut_gene.append("1")
                else:
                    mut_gene.append(bit)
            mut_gene_bin = ''.join(mut_gene)
            bound_flag = bound_check(mut_gene_bin)
            if bound_flag:
                return mut_gene_bin
            else:
                return mut_gene_bin[0]+"10011100010000"

        par_1 = self.individuals[par_1_index]
        par_2 = self.individuals[par_2_index]

        if random.randint(0, 100) >= self.cross_rate: # Define se o cruzamento ocorre. Se nao, retorna os pais
            return par_1, par_2

        cut = random.randint(1, 13)
        par_1_bin_x = [par_1.bin_x[:cut], par_1.bin_x[cut:]]
        par_1_bin_y = [par_1.bin_y[:cut], par_1.bin_y[cut:]]
        par_2_bin_x = [par_2.bin_x[:cut], par_2.bin_x[cut:]]
        par_2_bin_y = [par_2.bin_y[:cut], par_2.bin_y[cut:]]
        child_1_bin = [par_1_bin_x[0]+par_2_bin_x[1], par_1_bin_y[0]+par_2_bin_y[1]]
        child_2_bin = [par_2_bin_x[0]+par_1_bin_x[1], par_2_bin_y[0]+par_1_bin_y[1]]
        print(child_1_bin)

        child_1_bin = [mutation(child_1_bin[0], self.mutation_rate), mutation(child_1_bin[1], self.mutation_rate)]
        child_2_bin = [mutation(child_2_bin[0], self.mutation_rate), mutation(child_2_bin[1], self.mutation_rate)]

        return child_1_bin, child_2_bin

    def tournament(self, sample_size):
        sample = random.sample(self.individuals, sample_size)
        print(sample)
    
    #def initNewGeneration(self):

            

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

a = population(100, 1, 0.05)
a.plotGraph()
