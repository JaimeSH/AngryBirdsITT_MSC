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
import random
import subprocess
import os

class Selection:
    def __init__(self, root, path, inf):
        # Add entries to this list in order to be able to be used
        self.project_root = root
        self.game_path_tourney = path
        self.info = inf
        self.Selection_List = [self.Random_Selection, self.Tournament_Selection]
        pass
    
    def Selection_Base(self, population, limit, selection):
        S_Event = self.Selection_List[selection]
        return S_Event(population, limit)

    def Random_Selection(self, population, limit):
        # Generate a random number to select a parent
        tourney_members = []
        tourney_members_number = []
        pr = 1
        
        # Obtain two random members of the population (with replacement) to compete
        while pr <= limit:
            r = random.randint(0, (len(population)-1))
            tourney_members.append(population[r])
            tourney_members_number.append(r)
            pr = pr + 1
        
        # Return a randomly selected parent to add to the list
        #print("Llegue a Random")
        return tourney_members

    def Tournament_Selection(self, population, limit):
        ind_c = 0
        tourney_members = []
        tourney_members_number = []
        pr = 1
        
        # Obtain two random members of the population (with replacement) to compete
        while pr <= limit:
            r = random.randint(0, (len(population)-1))
            tourney_members.append(population[r])
            tourney_members_number.append(r)
            pr = pr + 1
                

        # Generate an XML to check the fitness
        for ind in tourney_members:
            ind.combine_mask()
            ind.generate_xml_tourney(individual = ind_c)
            ind_c = ind_c + 1

        # Execute the application with the two memebers
        subprocess.call(r'"' + os.path.join(self.project_root, self.game_path_tourney) + '"', startupinfo=self.info)
        
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
        return_list = []
        while len(tourney_members) != 0:
            winner = 0
            num_list = []
            if tourney_members[0].Fitness > tourney_members[1].Fitness:
                winner = tourney_members_number[0]
            elif tourney_members[1].Fitness > tourney_members[0].Fitness:
                winner = tourney_members_number[1]
            else:
                num_list.append(tourney_members_number[0])
                num_list.append(tourney_members_number[1])
                winner = random.choice(num_list)
            return_list.append(winner)
            tourney_members.pop(0)
            tourney_members.pop(0)

        # Finally return the winner of the tourney
        return return_list