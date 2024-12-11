fits = [-102, -4, -189, -20.5, 0.1, 0.5, -190]
new_gen = []

elite_index = []
for i in range(3):
    max_fit = -200
    index = 0
    for j, ind in enumerate(fits):
        if ind > max_fit and j not in elite_index: 
            max_fit = ind
            index = j
    elite_index.append(index)

print(elite_index)            
new_gen.append(max_fit)
fits = new_gen