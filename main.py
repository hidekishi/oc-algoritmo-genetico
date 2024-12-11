import lib

oc = lib.population(5000, 0.8, 0.01, 0.01)
oc.initFirstGen()

for i in range(20):
    oc.displayResults()
    oc.initNewGeneration(500)