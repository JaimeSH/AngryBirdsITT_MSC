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
max_gen = 100       # Max number of generations
fits = [0]           # Variable to save the fitness of each generation
gen = 1             # Generation 1
per_cross = 0.5     # Percentage of cross-over (cross-over operator)
per_comb = 0.3      # Percentage of combination (combination operator)
per_mut = 0.4       # Percentage of mutation
cross_type = 0      # Type of cross-over [ 0: One point CO - 1: Random point CO - TBD]
ind_pieces = 10     # Number of pieces that define an individual


## "Dictionary" to save the base pieces and structures

BLOCK_TYPE = {
    'Circle': {'height': 72, 'lenght': 72},
    'RectTiny': {'height': 22, 'lenght': 42},
    'RectSmall': {'height': 22, 'lenght': 42},
    'RectBig': {'height': 22, 'lenght': 42},
    'RectMedium': {'height': 22, 'lenght': 42},
    'RectFat': {'height': 42, 'lenght': 82},
    'SquareTiny': {'height': 22, 'lenght': 22},
    'SquareSmall': {'height': 42, 'lenght': 42},
    'Triangle': {'height': 72, 'lenght': 72},
    'TriangleHole': {'height': 82, 'lenght': 82},
    'SquareHole': {'height': 82, 'lenght': 82}
}

BLOCK_MATERIAL = {
    'wood': 0,
    'stone': 1,
    'ice': 2
}

## Block construction sequence
BLOCKS = {
    0: [
        {'type': BLOCK_TYPE['Circle'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    1: [
        {'type': BLOCK_TYPE['RectTiny'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    2: [
        {'type': BLOCK_TYPE['RectSmall'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    3: [
        {'type': BLOCK_TYPE['RectMedium'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    4: [
        {'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    5: [
        {'type': BLOCK_TYPE['RectFat'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    6: [
        {'type': BLOCK_TYPE['SquareTiny'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    7: [
        {'type': BLOCK_TYPE['SquareSmall'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    8: [
        {'type': BLOCK_TYPE['SquareHole'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    9: [
        {'type': BLOCK_TYPE['Triangle'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    10: [
        {'type': BLOCK_TYPE['TriangleHole'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 0, 0] # x, y, z - Calculated from the center of the figure
        }],
    11: [
        {'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, -91, 0] # x, y, z - Calculated from the center of the figure
        },
        {'type': BLOCK_TYPE['RectMedium'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [-90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'type': BLOCK_TYPE['RectMedium'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 91, 0] # x, y, z - Calculated from the center of the figure
        }],
    12: [
        {'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, -31, 0] # x, y, z - Calculated from the center of the figure
        },
        {'type': BLOCK_TYPE['RectTiny'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [-90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'type': BLOCK_TYPE['RectTiny'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [90, 0, 90] # x, y, z - Calculated from the center of the figure
        },
        {'type': BLOCK_TYPE['RectBig'],
        'material': BLOCK_MATERIAL['wood'],
        'offset': [0, 31, 0] # x, y, z - Calculated from the center of the figure
        }]
}


#####################################################################
########################< Class Definitions >########################
#####################################################################

class Composite:
    def __init__(self, blocks):
        # Blocks must be a list
        self.block = blocks

    def height(self):
        # Calculate height for blocks
        return 0.0

    def width(self):
        return 0.0

    def top_center(self):
        return 0.0

    def as_dictionary(self):
        return {}
    
    def as_json(self):
        return {}

Composites = {
    0: Composite(BLOCKS[0]),
    1: Composite(BLOCKS[11])
}

## Example of a basic chromosome (a list of connected composites)

chromosome = [0, 1, 0]

## When evaluating fitness or positiioning in map

chromosome_objects = [Composites[composite] for composite in chromosome]

for c in chromosome_objects:
    print(c.height())

class Individual:
    def __init__(self, **kwargs):
        #self.id = kwargs['id']
        #self.fitness = kwargs.get('fitness', {})
        self.chromosome = kwargs.get('chromosome', [])
        self.__dict__.update(kwargs)
        self.chromosome_objects = [Composites[composite] for composite in chromosome]

    def position_chromosome(self):
        #To do
        # Here you can use the chromosome objects etc.
        pass
    
    
    
pop = [ Individual(chromosome = [random.randint(0,1) for p in range(3)]) for i in range(10)]

for ind in pop:
    for gen ind.chromosome_objects:
        print(gen.blocks)