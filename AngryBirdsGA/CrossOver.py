from AngryBirdsGA import *

def SinglePoint(father, mother):
    # Generate a copy of each parent for the cross-over operation
    father = pop[parents[cross_parent] -1 ].chromosome
    mother = pop[parents[cross_parent + 1] - 1].chromosome
        
    # "Divide" the parents chromosomes for the operation
    father1 = father[0:math.floor(ind_pieces/2)]
    father2 = father[math.floor(ind_pieces/2):]
        
    mother1 = mother[0:math.floor(ind_pieces/2)]
    mother2 = mother[math.floor(ind_pieces/2):]
        
    # Generate the childs of both parents
    son = father1 + mother2
    daughter = mother1 + father2
    return 0

def DoublePoint(father, mother, p1, p2):
    # This mehtod uses predefined points for the crossover of the childs
    # the points are the same for all childs

    # Generate a copy of each parent for the cross-over operation
    father = pop[parents[cross_parent] -1 ].chromosome
    mother = pop[parents[cross_parent + 1] - 1].chromosome
        
    # "Divide" the parents chromosomes for the operation
    father1 = father[0:p1]
    father2 = father[(p1+1):p2]
    father3 = father[(p2+1):]
        
    mother1 = mother[0:p1]
    mother2 = mother[(p1+1):p2]
    mother3 = mother[(p2+1):]
        
    # Generate the childs of both parents
    son = father1 + mother2 + father3
    daughter = mother1 + father2 + mother3
    return 0

def UniformCross(father, mother):
    # This mehtod uses an uniform crossover mask to define
    # the elements that will be interchanged for the next
    # generations in the population

    father = pop[parents[cross_parent] -1 ].chromosome
    mother = pop[parents[cross_parent + 1] - 1].chromosome

    # We initialize the mask with the lenght of the bigger parent
    value = 0
    if len(father) >= len(mother):
        value = len(father)
        large = father
        short = mother
    else:
        value = len(mother)
        short = father
        large = mother
    
    mask = [random.randint(0,1) for a in range(value)]

    # We then interchange the values on both parents using the
    # generated mask

    for g in range(value):
        if mask[g] == 1:
            if g > len(short):
                short.append(large[g])
                large[g] = -1
            else:
                temp = short[g]
                short[g] = large[g]
                large[g] = temp
    
    # Remove -1 values from the larger parent
    while true:
        if -1 in large:
            large.remove(-1)
        else:
            break
    
    # Generate the childs of both parents order does not matter
    son = large
    daughter = short
    return 0