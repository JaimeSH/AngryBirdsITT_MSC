#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 12:37:00 2018

@author: Salinas Hernandez Jaime
"""

import random
import math

#
import datetime
import time
import os
import json
import sys
import XmlHelpers as xml
#--import AngryBirdsGA.XmlHelpers_mod as xml

__author__ = "Salinas Hernandez Jaime"
__copyright__ = "Copyright 2018, Tijuana Institute of Technology"
__credits__ = ["Dr. Mario García Valdez",""]
__license__ = "ITT"
__version__ = "1.0.3"
__date__ = "October 29, 2018 12:38"
__maintainer__ = "Salinas Hernandez Jaime"
__email__ = "jaime.salinas@tectijuana.edu.mx"
__status__ = "Development"



## Values used for the genetic algorithm
population = 10     # For now it can only be below 10
max_gen = 2       # Max number of generations
fits = [0]           # Variable to save the fitness of each generation
gen = 1             # Generation 1
per_cross = 0.5     # Percentage of cross-over (cross-over operator)
per_comb = 0.3      # Percentage of combination (combination operator)
per_mut = 0.4       # Percentage of mutation
cross_type = 0      # Type of cross-over [ 0: One point CO - 1: Random point CO - TBD]
ind_pieces = 10     # Number of pieces that define an individual


## Data required to create the xml files

#####################################################################
##############< Data required to create the xml files >##############
#####################################################################

project_root = os.getcwd()
config_param = json.loads(open("ga_parameters.json","r").read())

game_path = config_param['game_path']
write_path = config_param['write_path']
read_path = config_param['read_path']
log_path = config_param['log_dir']
log_base_name = config_param['log_base_name']
os.makedirs(os.path.join(project_root, log_path), exist_ok=True)

#os.system(game_path)


## "Dictionary" to save the base pieces and structures

BLOCK_TYPE = {
    'Circle': {'height': 72, 'lenght': 72},
    'RectTiny': {'height': 22, 'lenght': 42},
    'RectSmall': {'height': 22, 'lenght': 82},
    'RectBig': {'height': 22, 'lenght': 182},
    'RectMedium': {'height': 22, 'lenght': 162},
    'RectFat': {'height': 42, 'lenght': 82},
    'SquareTiny': {'height': 22, 'lenght': 22},
    'SquareSmall': {'height': 42, 'lenght': 42},
    'Triangle': {'height': 72, 'lenght': 72},
    'TriangleHole': {'height': 82, 'lenght': 82},
    'SquareHole': {'height': 82, 'lenght': 82}
}

BLOCK_MATERIAL = {
    0: 'wood',
    1: 'stone',
    2: 'ice'
}

# Generation masks
type_small_l = [[0,0,0,0,0,0],
                [0,0,1,0,0,0],
                [0,0,1,1,0,0]]
type_large_l = [[0,0,1,0,0,0],
                [0,0,1,0,0,0],
                [0,0,1,1,0,0]]
type_small_cube = [[0,0,0,0,0,0],
                   [0,0,1,1,0,0],
                   [0,0,1,1,0,0]]
type_large_cube = [[0,1,1,1,0,0],
                   [0,1,1,1,0,0],
                   [0,1,1,1,0,0]]
type_small_floor = [[0,0,0,0,0,0],
                    [0,0,0,0,0,0],
                    [0,1,1,1,1,0]]
type_large_floor = [[0,0,0,0,0,0],
                    [0,0,0,0,0,0],
                    [1,1,1,1,1,1]]
type_castle = [[0,0,1,1,0,0],
               [1,0,1,1,0,1],
               [1,1,1,1,1,1]]
type_house = [[0,0,1,1,0,0],
              [0,1,1,1,1,0],
              [0,1,1,1,1,0]]
type_towers = [[1,0,1,0,1,0],
               [1,0,1,0,1,0],
               [1,0,1,0,1,0]]

## Block construction sequence
BLOCKS = {
    0: [
        {'name': 'Circle',
        'type': BLOCK_TYPE['Circle'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    1: [
        {'name': 'RectTiny',
        'type': BLOCK_TYPE['RectTiny'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    2: [
        {'name': 'RectSmall',
        'type': BLOCK_TYPE['RectSmall'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    3: [
        {'name': 'RectMedium',
        'type': BLOCK_TYPE['RectMedium'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    4: [
        {'name': 'RectBig',
        'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    5: [
        {'name': 'RectFat',
        'type': BLOCK_TYPE['RectFat'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    6: [
        {'name': 'SquareTiny',
        'type': BLOCK_TYPE['SquareTiny'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    7: [
        {'name': 'SquareSmall',
        'type': BLOCK_TYPE['SquareSmall'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    8: [
        {'name': 'SquareHole',
        'type': BLOCK_TYPE['SquareHole'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    9: [
        {'name': 'Triangle',
        'type': BLOCK_TYPE['Triangle'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    10: [
        {'name': 'TriangleHole',
        'type': BLOCK_TYPE['TriangleHole'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    11: [
        {'name': 'RectBig',
        'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, -91, 0] # x, y, z - Calculated from the center of the figure
        },
        {'name': 'RectMedium',
        'type': BLOCK_TYPE['RectMedium'],
        'material': BLOCK_MATERIAL[0],
        'offset': [-90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'name': 'RectMedium',
        'type': BLOCK_TYPE['RectMedium'],
        'material': BLOCK_MATERIAL[0],
        'offset': [90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'name': 'RectBig',
        'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 91, 0] # x, y, z - Calculated from the center of the figure
        }],
    12: [
        {'name': 'RectBig',
        'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, -31, 0] # x, y, z - Calculated from the center of the figure
        },
        {'name': 'RectTiny',
        'type': BLOCK_TYPE['RectTiny'],
        'material': BLOCK_MATERIAL[0],
        'offset': [-90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'name': 'RectTiny',
        'type': BLOCK_TYPE['RectTiny'],
        'material': BLOCK_MATERIAL[0],
        'offset': [90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'name': 'RectBig',
        'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL[0],
        'offset': [0, 31, 0] # x, y, z - Calculated from the center of the figure
        }]
}


#####################################################################
########################< Class Definitions >########################
#####################################################################

class Composite:
    
    bl_list_x = []
    bl_list_y = []
    
    def __init__(self, blocks):
        # Blocks must be a list
        self.bl_list_x = []
        self.bl_list_y = []
        self.blocks = blocks
        self.get_values()
        self.height = self.height()
        self.width = self.width()
        self.top_center = self.top_center()
        self.as_dictionary = self.as_dictionary()
        
    def get_values(self):
        #print(self.blocks)
        for bl in self.blocks:
            #print(bl)
            self.bl_list_x.append(bl['offset'][0])
            self.bl_list_y.append(bl['offset'][1])
        #print("1")
        return 0

    def height(self):
        summ = 0
        if len(self.bl_list_y) == 1:
            for bl in self.blocks:
                offrot = bl['offset'][2]
                if offrot == 0:
                    summ = bl['type']['height'] # abs(bl['type']['lenght'])
                else:
                    summ = bl['type']['lenght'] # abs(bl['type']['height'])
        else:
            #print(self.blocks['offset'])
            for i in self.bl_list_y:
                summ = summ + abs(i)
            #summ = sum(self.bl_list_y)
            c = 0
            for bl in self.blocks:
                if self.bl_list_y[c] != 0:
                    offrot = bl['offset'][2]
                    if offrot == 0:
                        summ = summ + (bl['type']['height']/2) # abs(bl['type']['lenght'])
                    else:
                        summ = summ + (bl['type']['lenght']/2) # abs(bl['type']['height'])
                c = c + 1
        return summ
        #return 0.0

    def width(self):
        summ = 0
        if len(self.bl_list_x) == 1:
            for bl in self.blocks:
                offrot = bl['offset'][2]
                if offrot == 0:
                    summ = bl['type']['lenght'] # abs(bl['type']['lenght'])
                else:
                    summ = bl['type']['height'] # abs(bl['type']['height'])
        else:
            for i in self.bl_list_x:
                summ = summ + abs(i)
            c = 0
            for bl in self.blocks:
                if self.bl_list_x[c] != 0:
                    offrot = bl['offset'][2]
                    if offrot == 90:
                        summ = summ + (bl['type']['height']/2) # abs(bl['type']['height'])
                    else:
                        summ = summ + (bl['type']['lenght']/2) # abs(bl['type']['lenght'])
                c = c + 1
        return summ

    def top_center(self):
        height_center = self.height
        lenght_center = self.width/2
        return [lenght_center, height_center]

    def as_dictionary(self):
        block_list = []
        block_list.append([self.width, self.height])
        for piece in self.blocks:
            block_comp = []
            block_comp.append(piece['name'])
            block_comp.append(piece['material'])
            block_comp.append(piece['offset'][0])
            block_comp.append(piece['offset'][1])
            block_comp.append(piece['offset'][2])
            #block_comp.append([piece['name'], piece['material'], piece['offset'][0], piece['offset'][1], piece['offset'][2]])
            block_list.append(block_comp)
        #block_list.append(block_comp)
        #print(block_list)
        return block_list
    
    def as_json(self):
        return {}

Composites = {
    0: Composite(BLOCKS[0]),
    1: Composite(BLOCKS[1]),
    2: Composite(BLOCKS[2]),
    3: Composite(BLOCKS[3]),
    4: Composite(BLOCKS[4]),
    5: Composite(BLOCKS[5]),
    6: Composite(BLOCKS[6]),
    7: Composite(BLOCKS[7]),
    8: Composite(BLOCKS[8]),
    9: Composite(BLOCKS[9]),
    10: Composite(BLOCKS[10]),
    11: Composite(BLOCKS[11]),
    12: Composite(BLOCKS[12])
}

## Example of a basic chromosome (a list of connected composites)

chromosome = [0, 12, 0]

## When evaluating fitness or positiioning in map

chromosome_objects = [Composites[composite] for composite in chromosome]
tot_height = 0
#for c in chromosome_objects:
    #c.__height = c.height + c.__height
    #tot_height = tot_height + c.height()
#    print(c.height())


class Individual:
    def __init__(self, **kwargs):
        #self.id = kwargs['id']
        #self.fitness = kwargs.get('fitness', {})
        self.chromosome = kwargs.get('chromosome', [])
        self.__dict__.update(kwargs)
        self.chromosome_objects = [Composites[composite] for composite in self.chromosome]
        self.chromosome_coordinates = self.chromosome_coordinates()
        self.object_list = self.object_list()

    def position_chromosome(self):
        #To do
        # Here you can use the chromosome objects etc.
        pass
    
    def chromosome_coordinates(self):
        
        return [0, 0]
    
    def object_list(self):
        final_list = []
        #final_list.append(self.chromosome_coordinates)
        for com in self.chromosome_objects:
            obj_list =[]
            obj_list.append(com.as_dictionary)
            #obj_list.append([self.chromosome_coordinates[0], self.chromosome_coordinates[1]])
            final_list.append(obj_list)
        return final_list
    
    def generate_xml(self, **kwargs):
        #print(self.object_list)
        #os.path.join(write_path, "level-" + str(len(evaluated)).zfill(fill) + ".xml"))
        res_list = []
        res_list = xml.writeXML(self.object_list, os.path.join(project_root, write_path + "/level-0"+ str(kwargs.get('individual')) +".xml"))
        self.ind_height = res_list[0]
        self.ind_piece = res_list[1]
        #print("XML Completo")
        pass
    
    def read_xml(self, **kwargs):
        self.ind_piece_count = xml.readXML(os.path.join(project_root, read_path + "/level-"+ str(kwargs.get('individual')) +".xml"))
        pass
    
    def ind_height(self):
        return 0
    
    def ind_piece(self):
        return 0
    
    def ind_piece_count(self):
        return 0
    
    
    
pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)]) for i in range(population)]
"""
for ind in pop:
    for gen in ind.chromosome_objects:
        #print(gen.blocks)
        #print('')
        pass
"""    
    

while gen < max_gen: #and max(fits) < 100:
    #fits = [0]
    # If the current generation is not the first one generate a new population
    if gen != 1:
        # Determine via a random number which pieces to assign
        pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)]) for i in range(population)]
            
    # Outside IF statement
    
    # Check if the current number of population multiplied by the cross-over percentage
    # is an even or odd number, in the later case remove 1 from the value
    many = len(pop) * per_cross
    if many % 2 == 0:
        pass
    else:
        many = many - 1
    
    # Obtain the "parents" of the generation
    parents = []
    pr = 1
    while pr <= many:
        r = random.randint(1, population)
        if r not in parents: 
            parents.append(r)
            pr = pr + 1
            
    # Generate the cross-over operation (one-point crossover)
    for cross_parent in range(0, len(parents), 2):
        # Generate a copy of each parent for the cross-over operation
        father = pop[parents[cross_parent] -1 ].chromosome
        mother = pop[parents[cross_parent + 1] - 1].chromosome
        
        # "Divide" the parents chromosomes for the operation
        father11 = father[0:math.floor(ind_pieces/2)]
        father12 = father[math.floor(ind_pieces/2):]
        
        mother11 = mother[0:math.floor(ind_pieces/2)]
        mother12 = mother[math.floor(ind_pieces/2):]
        
        # Generate the childs of both parents
        son = father11 + mother12
        daughter = mother11 + father12
        
        # Mutate the childs (by chance like throwing a 100 side dice)
        # If greater than the treshold then mutate
        chance = random.randint(1, 100)
        threshold = 100 - (100 * per_mut)
        if chance > threshold:
            var=0
            #print("Mutate")
        else:
            var=1
            #print("Not Mutate")
        
        
        # Replace the parents in the generation
        pop[parents[cross_parent] - 1].chromosome = son
        pop[parents[cross_parent + 1] - 1].chromosome = daughter
        
        pop[parents[cross_parent] - 1] = Individual(chromosome = son)
        pop[parents[cross_parent + 1] - 1] = Individual(chromosome = daughter)
        
    ind_c = 0
    # After the cross-over
    for ind in pop:
        ind.generate_xml(individual = ind_c)
        ind_c = ind_c + 1
    

    
    time.sleep(1)
    # Runs and instance of the game
    os.system('"' + os.path.join(project_root, game_path) + '"')

    time.sleep(1)
    ################################################################################
    #############################< ELITE selection >################################
    ################################################################################
    
    # Read the xml files and get the data
    ind_c = 0
    for ind in pop:
        ind.read_xml(individual = ind_c)
        ind_c = ind_c + 1

    # Obtain the height of each individual
    data = []
    c = 0
    for ind in pop:
        data.append([int(ind.ind_height), ind.ind_piece, ind.ind_piece_count, abs(ind.ind_piece - ind.ind_piece_count), c])
        c = c + 1
    
    # Order the list
    results = sorted(data, key=lambda x: x[3], reverse=True)
    
    # Obtain the minor difference from each individual
    
    # Increase value of the generation for the next cycle
    gen = gen + 1


