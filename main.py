import lib

oc = lib.population(5000, 0.7, 0.01, 0.01)
oc.initFirstGen()

for i in range(10):
    oc.displayResults()
    oc.initNewGeneration(2000)

oc.generalGraph()