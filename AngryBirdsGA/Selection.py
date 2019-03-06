# Selection types for the population
#   - Random Selection
#   - Tournament Selection (best of)
#   - Future implementations
#
# After adding a new selection operation modify the 'Selection_List'
# at the end of the file
# 
#####################################################################################
#
# First the code reaches the 'Selection_Base' method and then is guided to the selection
# type that was decided on the main code, executes the procedure and returns a single member
# 
#
from class_oriented_idea import *
import random
import subprocess
import os

def Selection_Base(population, selection):
    S_Event = Selection_List[selection]
    return S_Event(population)

def Random_Selection(population):
    # Generate a random number to select a parent
    r = random.randint(1, population)
    best = population[r]
    
    # Return a randomly selected parent to add to the list
    print("Llegue a Random")
    return best

def Tournament_Selection(population):
    ind_c = 0
    tourney_members = []
    pr = 1
    
    # Obtain two random members of the population (with replacement) to compete
    while pr <= 2:
        r = random.randint(0, (len(population)-1))
        if r not in tourney_members: 
            tourney_members.append(population[r])
            pr = pr + 1

    # Generate an XML to check the fitness
    for ind in tourney_members:
        ind.combine_mask()
        ind.generate_xml_tourney(individual = ind_c)
        ind_c = ind_c + 1

    # Execute the application with the two memebers
    subprocess.call(r'"' + os.path.join(project_root, game_path_tourney) + '"', startupinfo=info)
    
    # Read the xml files and get the data
    ind_c = 0
    final_ind_list = []
    for ind in tourney_members:
        value = ind.read_xml(individual = ind_c)
        final_ind_list.append(value)
        #print(value)
        ind_c = ind_c + 1

    # Calculate the fitness for each individual
    for ind in tourney_members:
        ind.get_fitness()
        pass
    
    # Select the best of the two individuals of the tourney
    # in case both have the same fitness then chose one at random
    winner = 0
    if tourney_members[0].Fitness > tourney_members[1].Fitness:
        winner = tourney_members[0]
    elif tourney_members[1].Fitness > tourney_members[0].Fitness:
        winner = tourney_members[1]
    else:
        winner = random.choice(tourney_members)

    # Finally return the winner of the tourney
    return winner


# Add entries to this list in order to be able to be used
Selection_List = [Random_Selection, Tournament_Selection]