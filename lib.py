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
    def __init__(self, pop_size, cross_rate, mutation_rate, elite):
        self.pop_size = pop_size
        self.generation = 1
        self.mutation_rate = mutation_rate*100 # Para realizar operacoes com inteiros ao inves de float
        self.cross_rate = cross_rate*100       # Idem
        self.elite_pop = int(elite*pop_size)
        self.individuals = self.initFirstGen()
        self.average_fit = -200
    
    def initFirstGen(self):
        pop = []
        fit_sum = 0
        for i in range(self.pop_size):
            pop.append(individual(random.randint(-10000, 10000)/1000, random.randint(-10000, 10000)/1000))
            #print(pop[i].real_x, pop[i].real_y, pop[i].fit)
            fit_sum += pop[i].fit
        self.average_fit = fit_sum/self.pop_size
        return pop
    
    def plotGraph(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        x = []
        y = []
        z = []

        for ind in self.individuals:
            x.append(ind.real_x)
            y.append(ind.real_y)
        z = fitFunc(x, y)

        ax.scatter(x, y, z, color='red', s=10, label='Points', alpha=0.01)

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
        plt.close(fig)

    def displayResults(self):
        self.plotGraph()
        filename = "./fitness/"+str(self.generation)+"gen.txt"
        data = self.average_fit

        # Open the file in write mode ('w')
        with open(filename, "w") as file:
            file.write(str(data))


    def cross(self, par_1, par_2): # Cruzamento por 1 ponto aleatorio

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

        if random.randint(0, 100) >= self.cross_rate: # Define se o cruzamento ocorre. Se nao, retorna os pais
            return [par_1.real_x, par_1.real_y], [par_2.real_x, par_2.real_y]

        cut = random.randint(1, 13)
        par_1_bin_x = [par_1.bin_x[:cut], par_1.bin_x[cut:]]
        par_1_bin_y = [par_1.bin_y[:cut], par_1.bin_y[cut:]]
        par_2_bin_x = [par_2.bin_x[:cut], par_2.bin_x[cut:]]
        par_2_bin_y = [par_2.bin_y[:cut], par_2.bin_y[cut:]]
        child_1_bin = [par_1_bin_x[0]+par_2_bin_x[1], par_1_bin_y[0]+par_2_bin_y[1]]
        child_2_bin = [par_2_bin_x[0]+par_1_bin_x[1], par_2_bin_y[0]+par_1_bin_y[1]]

        child_1_bin = [mutation(child_1_bin[0], self.mutation_rate), mutation(child_1_bin[1], self.mutation_rate)]
        child_2_bin = [mutation(child_2_bin[0], self.mutation_rate), mutation(child_2_bin[1], self.mutation_rate)]

        return [binaryToReal(child_1_bin[0]), binaryToReal(child_1_bin[1])], [binaryToReal(child_2_bin[0]), binaryToReal(child_2_bin[1])]

    def sampling(self, sample_size): # Selecao por torneio

        def select_ind(sample):
            max_fit = -200
            max_fit_index = 0
            for i, ind in enumerate(sample):
                if ind.fit > max_fit:
                    max_fit = ind.fit
                    max_fit_index = i
            return sample[max_fit_index]

        sample = random.sample(self.individuals, sample_size)

        par_1 = select_ind(sample[:int(sample_size/2)])
        par_2 = select_ind(sample[int(sample_size/2):])

        return par_1, par_2
    
    def initNewGeneration(self, sample_size):
        #print(len(self.individuals))

        def eliteSelect():
            elite_index = []
            for i in range(self.elite_pop):
                max_fit = -200
                index = 0
                for j, ind in enumerate(self.individuals):
                    if ind.fit > max_fit and j not in elite_index: 
                        max_fit = ind.fit
                        index = j
                elite_index.append(index)
            return elite_index

        new_gen = []

        elite_index = eliteSelect()
        for i in elite_index:
            new_gen.append(self.individuals[i])

        for i in range(self.elite_pop, self.pop_size):
            par_1, par_2 = self.sampling(sample_size)
            child_1_genes, child_2_genes = self.cross(par_1, par_2)
            #print(child_1_genes, child_2_genes)
            child_1 = individual(child_1_genes[0], child_1_genes[1])
            child_2 = individual(child_2_genes[0], child_2_genes[1])

            new_gen.append(child_1)
            if len(new_gen) == self.pop_size:
                break
            new_gen.append(child_2)

        fit_sum = 0
        for ind in new_gen:
            fit_sum += ind.fit

        self.average_fit = fit_sum/self.pop_size
        self.individuals = new_gen
        self.generation += 1
            

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

a = population(5000, 0.8, 0.01, 0.01)
a.initFirstGen()
a.displayResults()
for i in range(20):
    a.displayResults()
    a.initNewGeneration(1000)