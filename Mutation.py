# Mutation Type for population
#   - Movement Mutation
#       - Gaussian mutation
#       - Fixed value movement
#   - Structure material mutation
#       - Random value
#   - Stucture type mutation
#       - Random value
#
#####################################################
#
# 
#
#
#
import random
import subprocess
import os
import math
import numpy as np

class Mutation:
    def __init__(self, percentage, mu, sigma, restrictions):
        self.M_Per = percentage
        self.mu = mu
        self.sigma = sigma
        self.Restricted = restrictions
        self.Material = ["wood", "ice", "stone"]
        self.Individual_list = [self.Add_Rand, self.Del_Rand]
        self.Movement_list = [self.Move_Gauss, self.Move_Fixed]
        self.Material_list = [self.Mate_Rand]
        self.Structure_list = [self.Struc_Rand]
        pass

    def UpdateComposites(self, Composites):
        self.Composites = Composites
        pass
    
    def UpdateNDValues(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma
    
    # Movement Mutation Group
    def M_Movement(self, individual, selection):
        M_Event = self.Movement_list[selection]
        return M_Event(individual)

    def Move_Gauss(self, individual):
        # Define how many elements to modify
        value = random.randint(0,len(individual.chromosome)-1)
        
        # Obtain as many normal distributed numbers as needed
        s = np.random.normal(self.mu, self.sigma, value)

        mod_list = []
        pr = 0
        while pr < value:
            r = random.randint(0, len(individual.chromosome)-1)
            if r not in mod_list:
                individual.Mut_Movement[r] = s[pr]
                mod_list.append(r)
                pr = pr + 1

        return individual

    def Move_Fixed(self, individual):
        # Define how many elements to modify
        value = random.randint(0,len(individual.chromosome)-1)

        mod_list = []
        pr = 0
        while pr <= value:
            r = random.randint(0, len(individual.chromosome)-1)
            if r not in mod_list: 
                individual.Mut_Movement[r] = 10
                mod_list.append(r)
                pr = pr + 1
        return individual
    
    # Structure TYPE Mutation Group
    def M_StrucType(self, individual, selection = 0):
        #M_Event = self.Material_list[selection]
        M_Event = self.Structure_list[selection]
        return M_Event(individual)

    def Struc_Rand(self, individual):
        # Define how many elements to modify
        value = random.randint(0,len(individual.chromosome)-1)

        mod_list = []
        pr = 0
        while pr <= value:
            r = random.randint(0, len(individual.chromosome)-1)
            if r not in mod_list:
                prop = random.randint(0, len(self.Composites)-1)
                if self.Restricted[self.Composites[prop][0][0]].Valid == True:
                    individual.Mut_Struct[r] = prop
                    #individual.Mut_Struct[r] = random.randint(0, len(self.Composites)-1)
                    mod_list.append(r)
                    pr = pr + 1
        return individual
            
    
    # Structure MATERIAL Mutation Group
    def M_StructMat(self, individual, selection = 0):
        M_Event = self.Material_list[selection]
        return M_Event(individual)

    def Mate_Rand(self, individual):
        # Define how many elements to modify
        value = random.randint(0,len(individual.chromosome)-1)

        mod_list = []
        pr = 0
        while pr <= value:
            r = random.randint(0, len(individual.chromosome)-1)
            if r not in mod_list: 
                individual.Mut_Material[r] = self.Material[random.randint(0, 2)]
                mod_list.append(r)
                pr = pr + 1
        return individual

    # Individual mutation
    def M_Individual(self, individual):
        M_Event = self.Individual_list[random.randint(0,1)]
        return M_Event(individual)

    def Add_Rand(self, individual):
        # Randmly add an element to the individual 
        rand = random.randint(0,100)
        if rand <= (self.M_Per*100):
            randpiece = random.randint(0, len(self.Composites)-1)
            individual.append(randpiece)
        return individual

    def Del_Rand(self, individual):
        # Check every element in a individual and randomly delete a single one
        p_deleted = False
        for v in range(0, len(individual)):
            rand = random.randint(0,100)
            if rand <= (self.M_Per*100):
                individual[v] = -1
                p_deleted = True

            # If a piece has been selected to be deleted then exit the loop    
            if p_deleted == True:
                break
        
        # Remove -1 values from the individual
        while True:
            if -1 in individual:
                individual.remove(-1)
            else:
                break

        return individual