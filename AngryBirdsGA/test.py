from class_oriented_idea import *
import random
import subprocess
import os

class Selection:
    def __init__(self, x, y, r):
        # Add entries to this list in order to be able to be used
        self.Selection_List = [self.Random_Selection, self.Tournament_Selection]
        pass
    
    def Selection_Base(self, population, selection):
        S_Event = self.Selection_List[selection]
        return S_Event(population)

    def Random_Selection(self, population):
        # Generate a random number to select a parent
        r = random.randint(1, population)
        best = population[r]
        
        # Return a randomly selected parent to add to the list
        print("Llegue a Random")
        return best

    def Tournament_Selection(self, population):
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