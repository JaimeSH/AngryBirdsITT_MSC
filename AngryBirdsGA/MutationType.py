from AngryBirdsGA import *

def RandomMutatio(individual, per):
    # Check every element in a individual and randomly change some
    for v in range(0, len(individual)):
        rand = random.randint(0,100)
        if rand <= (per*100):
            randpiece = random.randint(0, len(Composites)-1)
            individual[v] = randpiece
    return 0

def AddMutation(individual, per):
    # Randmly add an element to the individual 
    rand = random.randint(0,100)
    if rand <= (per*100):
        randpiece = random.randint(0, len(Composites)-1)
        individual.append(randpiece)
    return 0

def DelMutation(individual):
    # Check every element in a individual and randomly delete anyone
    for v in range(0, len(individual)):
        rand = random.randint(0,100)
        if rand <= (per*100):
            individual[v] = -1
    
    # Remove -1 values from the individual
    while true:
        if -1 in large:
            large.remove(-1)
        else:
            break

    return 0