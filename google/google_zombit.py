def answer(population, x, y, strength):
    #if patient z is strong enough, the virus never takes hold
    if population[y][x] > strength:
        return population
    
    #infect patient z
    population = population_after_infection(population, x, y)
    #new_patients are those which have been infected, but haven't infected others yet
    new_patients = [(x, y)] 
    while len(new_patients) != 0:
        #patient is going to infect its neighbors
        patient = new_patients.pop()
        patient_x = patient[0]
        patient_y = patient[1]
        for adjacent_patient in [(patient_x+1, patient_y), (patient_x-1, patient_y), (patient_x, patient_y+1), (patient_x, patient_y-1)]:         
            adjacent_x = adjacent_patient[0]
            adjacent_y = adjacent_patient[1]
            if position_in_bounds(population, adjacent_x, adjacent_y):
                resistance = population[adjacent_y][adjacent_x]
                if strength >= resistance and living_at_position(population, adjacent_x, adjacent_y ):
                    new_patients.insert(0, adjacent_patient)
                    #if the neighbors are weak enough and not infected, infect them
                    #and they get in line to infect their own neighbors
                    population = population_after_infection(population, adjacent_x, adjacent_y)

    return population


     
def population_after_infection(population, x, y):
    population[y][x] = -1
    return population
   
def position_in_bounds(population, x, y):
    return y < len(population) and y >= 0 and x < len(population[0]) and x >= 0

def living_at_position(population, x, y):
    return population[y][x] != -1
