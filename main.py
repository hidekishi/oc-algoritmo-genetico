import lib

pop_size = int(input("Tamanho da população: "))
cross_rate = float(input("Taxa de cruzamento (0-1): "))
mutation_rate = float(input("Taxa de mutação (0-1): "))
gen_num = int(input("Número de gerações: "))
sample_prop = float(input("Proporção da população para torneio (0-1): "))

oc = lib.population(pop_size, cross_rate, mutation_rate, 0.01)
oc.initFirstGen()


filename = "./output/avg_fitness.csv"
data = f"Geração\tFitness med.\tFitness max.\tx\ty\n"
with open(filename, "w") as file:
    file.write(str(data))

for i in range(gen_num):
    oc.displayResults()
    oc.initNewGeneration(int(pop_size*sample_prop))

oc.generalGraph()