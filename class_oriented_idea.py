from __future__ import division, absolute_import                 #to avoid integer devision problem
import datetime
import scipy
import pylab
#
import random
import math
#
import datetime
import time
import os
import json
import sys
import subprocess
import itertools
import operator

# Local files
import XmlHelpers as xml
import Evaluation as Eval
from Selection import Selection
from Mutation import Mutation

author = "Salinas Hernandez Jaime"
copyright = "Copyright 2018, Tijuana Institute of Technology"
credits = ["Dr. Mario García Valdez",""]
license = "ITT"
version = "1.3.2"
date = "March 07, 2019 17:40"
maintainer = "Salinas Hernandez Jaime"
email = "jaime.salinas@tectijuana.edu.mx"
status = "Development"
t_begin = datetime.datetime.now()


## Values used for the genetic algorithm
population = 10         # For now it can only be below 10
max_gen = 6            # Max number of generations
fits = [0]              # Variable to save the fitness of each generation
gen = 0                 # Generation 1
per_cross = 0.5         # Percentage of cross-over (cross-over operator)
per_comb = 0.3          # Percentage of combination (combination operator)
per_mut = 0.4           # Percentage of mutation
sel_type = 1            # Selection (for crossover) type [ 0: Random - 1: Tournament - TBD]
cross_type = 0          # Type of cross-over [ 0: One point CO - 1: Random point CO - TBD]
ind_pieces = 20         # Number of pieces that define an individual
all_fit = []            # Average fitness for all generations
fit_Alen = []           # Average piece length fitness for all generations
fit_Amov = []           # Average movement fitness for all generations
max_elite = 2           # Maximum number of elite members in the generation
elite = []
best_gen = []
mu = 0                  # Mean for normal distribution
sigma = 20              # SD for normal distribution

## Data required to create the xml files

#####################################################################
##############< Data required to create the xml files >##############
#####################################################################

project_root = os.getcwd()
config_param = json.loads(open("ga_parameters.json","r").read())

game_path = config_param['game_path']
write_path = config_param['write_path']
elite_path = config_param['elite_path']
read_path = config_param['read_path']
log_path = config_param['log_dir']
log_base_name = config_param['log_base_name']
os.makedirs(os.path.join(project_root, log_path), exist_ok=True)

# For tournament
game_path_tourney = config_param['game_path_tourney']
write_path_tourney = config_param['write_path_tourney']
read_path_tourney = config_param['read_path_tourney']

## "Dictionary" to save the base pieces and structures
SW_HIDE = 0
info = subprocess.STARTUPINFO()
info.dwFlags = subprocess.STARTF_USESHOWWINDOW
info.wShowWindow = SW_HIDE

#just for fun making further development easier and with joy
pi     = scipy.pi
dot    = scipy.dot
sin    = scipy.sin
cos    = scipy.cos
ar     = scipy.array
rand   = scipy.rand
arange = scipy.arange
plot   = pylab.plot
show   = pylab.show
axis   = pylab.axis
grid   = pylab.grid
title  = pylab.title
rad    = lambda ang: ang*pi/180                 #lovely lambda: degree to radian
sel_operator = Selection(project_root, game_path_tourney, info)
mut_operator = Mutation(per_mut, mu, sigma)


# Function to rotate points
def Rotate2D(pts,cnt,ang=pi/4):
    '''pts = {} Rotates points(nx2) about center cnt(2) by angle ang(1) in radian'''
    return dot(pts-cnt,ar([[cos(ang),sin(ang)],[-sin(ang),cos(ang)]]))+cnt


# Generation masks
type_small_l = [[0,0,0,0,0,0,0],
                [0,0,2,0,0,0,0],
                [0,0,1,1,0,0,0]]
type_large_l = [[0,0,3,0,0,0,0],
                [0,0,2,0,0,0,0],
                [0,0,1,1,0,0,0]]
type_small_cube = [[0,0,0,0,0,0,0],
                   [0,0,2,2,0,0,0],
                   [0,0,1,1,0,0,0]]
type_large_cube = [[0,3,3,3,0,0,0],
                   [0,2,2,2,0,0,0],
                   [0,1,1,1,0,0,0]]
type_small_floor = [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,1,1,1,1,1,0]]
type_large_floor = [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [1,1,1,1,1,1,1]]
type_castle = [[0,0,0,3,0,0,0],
               [2,0,2,2,2,0,2],
               [1,1,1,1,1,1,1]]
type_house = [[0,0,3,3,0,0,0],
              [0,2,2,2,2,0,0],
              [0,1,1,1,1,0,0]]
type_towers = [[3,0,3,0,3,0,0],
               [2,0,2,0,2,0,0],
               [1,0,1,0,1,0,0]]

Mask_List = [
    type_small_l,
    type_large_l,
    type_small_cube,
    type_large_cube,
    type_small_floor,
    type_large_floor,
    type_castle,
    type_house,
    type_towers
]

# Global Piece class and a class for each piece in the game
class Piece:
    def __init__(self, x, y, r):
        #self.Height = 72
        #self.Width = 72
        self.Material = "wood"
        self.Dict = []
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([self.Width/2 +       self.X,         self.Height/2 +     self.Y])
        ed_lis.append([self.Width/2 +       self.X, 0 -     self.Height/2 +     self.Y])
        ed_lis.append([0 - self.Width/2 +   self.X, 0 -     self.Height/2 +     self.Y])
        ed_lis.append([0 - self.Width/2 +   self.X,         self.Height/2 +     self.Y])
        self.Edges = ed_lis

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.Edges, ar([0 + self.X, 0 + self.Y]), ang)
        self.Points = ots.tolist()

    def change_material(self, m):
        self.Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.Name)
        self_list.append(self.Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.Dict = self_list
        
    def update_values(self):
        self.get_edges()
        self.get_points(self.R)
        self.as_dictionary()

class Circle(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "Circle"
        self.Height = 75
        self.Width = 75
        Piece.__init__(self, x, y, r)
        self.update_values()

class RectTiny(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectTiny"
        self.Height = 25
        self.Width = 45
        Piece.__init__(self, x, y, r)
        self.update_values()
    

class RectSmall(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectSmall"
        self.Height = 25
        self.Width = 85
        Piece.__init__(self, x, y, r)
        self.update_values()


class RectMedium(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectMedium"
        self.Height = 25
        self.Width = 165
        Piece.__init__(self, x, y, r)
        self.update_values()


class RectBig(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectBig"
        self.Height = 25
        self.Width = 185
        Piece.__init__(self, x, y, r)
        self.update_values()


class RectFat(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectFat"
        self.Height = 45
        self.Width = 85
        Piece.__init__(self, x, y, r)
        self.update_values()


class SquareTiny(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "SquareTiny"
        self.Height = 25
        self.Width = 25
        Piece.__init__(self, x, y, r)
        self.update_values()


class SquareSmall(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "SquareSmall"
        self.Height = 45
        self.Width = 45
        Piece.__init__(self, x, y, r)
        self.update_values()


class Triangle(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "Triangle"
        self.Height = 75
        self.Width = 75
        Piece.__init__(self, x, y, r)
        self.update_values()


class TriangleHole(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "TriangleHole"
        self.Height = 85
        self.Width = 85
        Piece.__init__(self, x, y, r)
        self.update_values()


class SquareHole(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "SquareHole"
        self.Height = 85
        self.Width = 85
        Piece.__init__(self, x, y, r)
        self.update_values()


# Composite class to control the generation of the individuals
class Composite:
    
    bl_list_x = []
    bl_list_y = []
    
    def __init__(self, blocks):
        # Blocks must be a list
        self.Objetos2 = []
        self.bl_list_x = []
        self.bl_list_y = []
        self.blocks = blocks.copy()
        self.Objetos = [clases[clase](x,y,r) for (clase,x,y,r) in self.blocks.copy()]
        self.get_values()
        self.height = self.height()
        self.width = self.width()
        self.top_center = self.top_center()
        self.as_dictionary = self.as_dictionary()
        
    def get_values(self):
        self.Borders = [[(x,y) for (x,y) in Obj.Points] for Obj in self.Objetos]
        self.Borders = sum(self.Borders, [])
        self.Width = abs(min(self.Borders, key=lambda t:t[0])[0] - max(self.Borders, key=lambda t:t[0])[0])
        self.Height = abs(min(self.Borders, key=lambda t:t[1])[1] - max(self.Borders, key=lambda t:t[1])[1])
        return 0

    def height(self):
        return 0.0

    def width(self):
        return 0.0
    
    def set_borders(self):
        
        return 0.0

    def top_center(self):
        height_center = self.Height
        lenght_center = self.Width/2
        return [lenght_center, height_center]

    def as_dictionary(self):
        block_list = []
        block_list.append([self.Width, self.Height])
        for piece in self.Objetos:
            block_comp = []
            block_comp.append(piece.Dict[0])
            block_comp.append(piece.Dict[1])
            block_comp.append(piece.Dict[2])
            block_comp.append(piece.Dict[3])
            block_comp.append(piece.Dict[4])
            block_list.append(block_comp)
        #block_list.append(block_comp)
        #print(block_list)
        return block_list
    
    def move_xy(self, n_x, n_y):
        self.Objetos = [clases[clase](x + n_x, y + n_y, r) for (clase,x,y,r) in self.blocks.copy()]
        return 0
    
    def as_json(self):
        return {}
   

clases = {
        "Circle":Circle,
        "RectTiny":RectTiny,
        "RectSmall":RectSmall,
        "RectMedium":RectMedium,
        "RectBig":RectBig,
        "RectFat":RectFat,
        "SquareTiny":SquareTiny,
        "SquareSmall":SquareSmall,
        "SquareHole":SquareHole,
        "Triangle":Triangle,
        "TriangleHole":TriangleHole }

clases1 = {
        "Circle":Circle
        }
"""
Composites = {
    0: Composite([("Circle", 0, 0, 90)]),
    1: Composite([("RectTiny", 0, 0, 90)]),
    2: Composite([("RectSmall", 0, 0, 90)]),
    3: Composite([("RectMedium", 0, 0, 90)]),
    4: Composite([("RectBig", 0, 0, 90)]),
    5: Composite([("RectFat", 0, 0, 90)]),
    6: Composite([("SquareTiny", 0, 0, 0)]),
    7: Composite([("SquareSmall", 0, 0, 0)]),
    8: Composite([("SquareHole", 0, 0, 0)]),
    9: Composite([("Triangle", 0, 0, -135)]),
    10: Composite([("TriangleHole", 0, 0, 0)]),
    11: Composite([("RectBig", 0, -91, 0), ("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)]),
    12: Composite([("RectBig", 0, -31, 0), ("RectTiny", -90, 0, 90), ("RectTiny", 90, 0, 90), ("RectBig", 0, 31, 0)]),
    13: Composite([("RectBig", 100, 5, -27), ("RectBig", -100, 5, 27), ("RectTiny", 0, 0, 90)]),
    14: Composite([("RectBig", 100, 5, -27), ("RectTiny", 0, 0, 90)]),
    15: Composite([("RectBig", -100, 5, 27), ("RectTiny", 0, 0, 90)]),
    16: Composite([("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)]),
    17: Composite([("RectMedium", 0, 0, 90), ("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)]),
    18: Composite([])
}

Composites = {
    0: [("RectBig", 0, -91, 0), ("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)],
    1: [("RectBig", 0, -31, 0), ("RectTiny", -90, 0, 90), ("RectTiny", 90, 0, 90), ("RectBig", 0, 31, 0)],
    2: [("RectBig", 100, 5, -27), ("RectBig", -100, 5, 27), ("RectSmall", 0, 0, 90)],
    3: [("RectBig", 100, 5, -27), ("RectSmall", 0, 0, 90)],
    4: [("RectBig", -100, 5, 27), ("RectSmall", 0, 0, 90)],
    5: [("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)],
    6: [("RectMedium", 0, 0, 90), ("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)]
}
"""
Composites = {
    0: [("RectBig", 0, -91, 0), ("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)],
    1: [("RectBig", 0, -31, 0), ("RectTiny", -90, 0, 90), ("RectTiny", 90, 0, 90), ("RectBig", 0, 31, 0)],
    2: [("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)],
    3: [("RectMedium", 0, 0, 90), ("RectMedium", -90, 0, 90), ("RectMedium", 90, 0, 90), ("RectBig", 0, 91, 0)],
    4: [("RectBig", 100, 5, -27), ("RectBig", -100, 5, 27), ("RectSmall", 0, 0, 90)]#,
    #5: [("RectTiny", 0, 0, 0)],
    #6: [("RectSmall", 0, 0, 0)],
    #7: [("RectMedium", 0, 0, 0)],
    #8: [("RectBig", 0, 0, 0)],
    #9: [("RectFat", 0, 0, 0)],
    #10: [("SquareSmall", 0, 0, 0)],
    #11: [("SquareHole", 0, 0, 0)],
    #12: [("Circle", 0, 0, 0)],
    #5: [("TriangleHole", 0, 0, 0)]
}

"""
BLOCK_LIST = [[]]
Blockes = [("SquareHole", 22, 22, 80),("SquareHole", 22, 22, 80),("TriangleHole", 22, 22, 80)]

objetos = [clases[clase](x,y,r) for (clase,x,y,r) in Blockes]


Bloque1 = [("Circle", 22,22,90),("SquareHole", 25, 30, 0)]
objetos = [clases[clase](x,y,r) for (clase,x,y,r) in Bloque1]


BLOCKS = {
0: [
    SquareHole(22,22,80),
    TriangleHole(12,23,90),
    RectBig(10,10,80),
    RectTiny(20,20,50)
]
}

for bl in BLOCKS[0]:
    bl.update_values()
    print(bl.Dict)
    print(bl.X)
    
    ***/
#clases = {
#        '1':SquareHole, 
#        '2':TriangleHole,
#        }
#clases["1"](22,22,80)
"""

################################################################################
#############################< Code Adaptation >################################
################################################################################

mut_operator.UpdateComposites(Composites)
#####################################################################
########################< Class Definitions >########################
#####################################################################

 
    
    
class Individual:
    def __init__(self, **kwargs):
        self.chromosome = kwargs.get('chromosome', [])
        self.mask = kwargs.get('mask') #self.assign_mask(Mask_List[kwargs.get('mask')])
        self.__dict__.update(kwargs)
        self.chromosome_objects = [Composite(Composites[composite]) for composite in self.chromosome]
        self.object_list = self.object_list_gen()
        self.object_masked = []
        self.Mut_Movement = [0 for value in self.chromosome]
        self.Mut_Struct = [-1 for value in self.chromosome]
        self.Mut_Material = [0 for value in self.chromosome]

    def position_chromosome(self):
        #To do
        # Here you can use the chromosome objects etc.
        pass
    
    def UpdateMutation(self):
        for c, struc in enumerate(self.Mut_Struct):
            if struc != -1:
                self.chromosome[c] = struc

        self.chromosome_objects = [Composite(Composites[composite]) for composite in self.chromosome]

        for mat in self.Mut_Material:
            for objeto in self.chromosome_objects:
                for pieza in objeto.Objetos:
                    if mat != 0:
                        pieza.Material = mat
                        pieza.update_values()
        
        for c, mov in enumerate(self.Mut_Movement):
            self.chromosome_objects[c].move_xy(mov, 0)

        self.object_list = self.object_list_gen()
        pass
    
    def chromosome_coordinates(self):
        
        return [0, 0]
    
    def object_list_gen(self):
        final_list = []
        for com in self.chromosome_objects:
            obj_list =[]
            obj_list.append(com.as_dictionary)
            final_list.append(obj_list)
        return final_list
    
    def generate_xml(self, **kwargs):
        res_list = []
        res_list = xml.writeXML(self.object_list, os.path.join(project_root, write_path + "/level-0"+ str(kwargs.get('individual')) +".xml"))
        self.ind_height = res_list[0]
        self.ind_piece = res_list[1]
        self.Pieces = res_list[2]
        pass
    
    def read_xml(self, **kwargs):
        self.Remaining_Pieces = xml.readXML(os.path.join(project_root, read_path + "/level-"+ str(kwargs.get('individual')) +".xml"))
        self.ind_piece_count = len(self.Remaining_Pieces)
        pass
    
    def read_xml_tourney(self, **kwargs):
        self.Remaining_Pieces = xml.readXML(os.path.join(project_root, read_path_tourney + "/level-"+ str(kwargs.get('individual')) +".xml"))
        self.ind_piece_count = len(self.Remaining_Pieces)
        pass
    
    def ind_height(self):
        return 0
    
    def ind_piece(self):
        return 0
    
    def ind_piece_count(self):
        return 0

    def assign_mask(self, mask_class):
        masked = mask_class
        print(masked)
        #self.mask = mask_class
        return masked
    
    def get_fitness(self):
        self.Fitness, self.Fit_Size, self.Fit_Pos = Eval.fitness(self.Pieces, self.Remaining_Pieces, self.chromosome)
        return 0
    
    def combine_mask(self):
        self.object_masked = xml.calculate_mask(self.object_list, self.mask)
        #self.object_list = xml.calculate_mask(self.object_list, type_castle)
        return 0
    def generate_xml_masked(self, **kwargs):
        res_list = []
        res_list = xml.writeXML_masked(self.object_list, os.path.join(project_root, write_path + "/level-0"+ str(kwargs.get('individual')) +".xml"))
        self.ind_height = res_list[0]
        self.ind_piece = res_list[1]
        self.Pieces = res_list[2]
        #print("XML Completo")
        pass
    
    def generate_xml_tourney(self, **kwargs):
        res_list = []
        res_list = xml.writeXML_masked(self.object_list, os.path.join(project_root, write_path_tourney + "/level-0"+ str(kwargs.get('individual')) +".xml"))
        self.ind_height_tourney = res_list[0]
        self.ind_piece_tourney = res_list[1]
        self.Pieces = res_list[2]
        pass

    def generate_xml_elite(self, **kwargs):
        res_list = []
        res_list = xml.writeXML_masked(self.object_list, os.path.join(project_root, elite_path + "/level-" + str(kwargs.get('gen')) + "0" + str(kwargs.get('individual'))  + ".xml"))
        self.ind_height = res_list[0]
        self.ind_piece = res_list[1]
        self.Pieces = res_list[2]
        pass
    
    
#pop_mask = [random.randint(0,len(Mask_List)-1) for i in range(population)]
pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)], mask = Mask_List[random.randint(0,len(Mask_List)-1)]) for i in range(population)]

#for c, ind in enumerate(pop):
#    ind.assign_mask(mask=pop_mask[c])
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
    ###if gen != 1:
    #    Determine via a random number which pieces to assign
    #   pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)]) for i in range(population)]
    ###
            
    # Outside IF statement
    # Reintegrate ELITE members if there are
    if len(elite):
        for member in elite:
            pop.insert(0, member)
            pop[0] = Individual(chromosome = member[1], mask = member[2])
            pop = pop[:population]

    # Check if the current number of population multiplied by the cross-over percentage
    # is an even or odd number, in the later case remove 1 from the value
    many = len(pop) * per_cross
    if many % 2 == 0:
        pass
    else:
        many = many - 1
    
    
    ### Discontinued since ver. 1.3.0
    #while pr <= many:
    #    parents.append(sel_operator.Selection_Base(pop, sel_type))
    #    Selection_Base(pop,1)
    #    r = random.randint(1, population)
    #    if r not in parents: 
    #        parents.append(r)
    #        pr = pr + 1
    ###

    # Combine the mask of the individual before entering the simulation
    ind_c = 0
    for ind in pop:
        ind.combine_mask()
        ind.generate_xml_masked(individual = ind_c)
        ind_c = ind_c + 1
    
    # Runs and instance of the game
    #subprocess.Popen(r'"' + os.path.join(project_root, game_path) + '"', startupinfo=info)  # doesn't capture output
    subprocess.call(r'"' + os.path.join(project_root, game_path) + '"', startupinfo=info)  # doesn't capture output

    # After the simulation obtain the fitness value for the population
    # Read the xml files and get the data
    ind_c = 0
    final_ind_list = []
    for ind in pop:
        value = ind.read_xml(individual = ind_c)
        final_ind_list.append(value)
        ind_c = ind_c + 1

    # Calculate the fitness for each individual
    for ind in pop:
        ind.get_fitness()
        pass

    ############################################################################
    #############################< Selection steps >############################
    ############################################################################
    # Obtain the "parents" of the generation
    parents = []
    pr = 1
    parents = sel_operator.Selection_Base(pop, many, sel_type)

    ############################################################################
    #############################< Crossover steps >############################
    ############################################################################
    
    new_members = []

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
        
        mask_son = Mask_List[random.randint(0,len(Mask_List)-1)]
        mask_daughter = Mask_List[random.randint(0,len(Mask_List)-1)]
        # Replace the parents in the generation
        pop[parents[cross_parent] - 1].chromosome = son
        pop[parents[cross_parent + 1] - 1].chromosome = daughter
        
        pop[parents[cross_parent] - 1] = Individual(chromosome = son, mask = mask_son)
        pop[parents[cross_parent + 1] - 1] = Individual(chromosome = daughter, mask = mask_daughter)

        # Mutate the childs (by chance like throwing a 100 side dice)
        # If greater than the treshold then mutate
        chance = random.randint(1, 100)
        threshold = 100 - (100 * per_mut)
        chance = 100
        if chance > threshold:
            var=0
            new_chrom = mut_operator.M_Individual(pop[parents[cross_parent] - 1].chromosome)
            pop[parents[cross_parent] - 1] = Individual(chromosome = new_chrom, mask = mask_son)
            pop[parents[cross_parent] - 1] = mut_operator.M_Movement(pop[parents[cross_parent] - 1], 0)
            pop[parents[cross_parent] - 1] = mut_operator.M_StructMat(pop[parents[cross_parent] - 1], 0)
            pop[parents[cross_parent] - 1] = mut_operator.M_StrucType(pop[parents[cross_parent] - 1], 0)
            pop[parents[cross_parent] - 1].UpdateMutation()
            #print("Mutate")
        else:
            var=1
            #print("Not Mutate")
        
        pop[parents[cross_parent] - 1].ind_c = parents[cross_parent] - 1
        pop[parents[cross_parent+1] - 1].ind_c = parents[cross_parent] - 1
        new_members.append(pop[parents[cross_parent] - 1])
        new_members.append(pop[parents[cross_parent + 1] - 1])
    
    # Calculate the new individuals fitness by sending them to a diferent simulation track
    
    # Generate an XML to check the fitness
    for ind_c, ind in enumerate(new_members):
        ind.combine_mask()
        ind.generate_xml_tourney(individual = ind_c)
    
    # Execute the application with the two memebers
    subprocess.call(r'"' + os.path.join(project_root, game_path_tourney) + '"', startupinfo=info)

    # Then obtain the remaining fitness values
    for ind in new_members:
        ind.read_xml_tourney(individual = ind.ind_c)
        ind.get_fitness()

    ### After the cross-ver
    ### Legacy Method    
    #ind_c = 0
    #for ind in pop:
    #    ind.generate_xml(individual = ind_c)
    #    ind_c = ind_c + 1
    ###

    ################################################################################
    #############################< ELITE selection >################################
    ################################################################################
    """
    # Obtain the height of each individual
    data = []
    c = 0
    for ind in pop:
        data.append([int(ind.ind_height), ind.ind_piece, ind.ind_piece_count, abs(ind.ind_piece - ind.ind_piece_count), c])
        c = c + 1
    
    # Order the list
    results = sorted(data, key=lambda x: x[3], reverse=True)
    """
    # Add the best individuals to the elite group
    

    # Obtain the average fitness of the generation
    gen_fit = 0
    len_fit = 0
    mov_fit = 0
    fit_pop = []
    for c, ind in enumerate(pop):
        fit_pop.append([c, ind.Fitness])
        gen_fit = gen_fit + ind.Fitness
        if c == 0:
            best_gen.append(ind.Fitness)
        len_fit += ind.Fit_Size
        mov_fit += ind.Fit_Pos
    
    fit_pop.sort(key=lambda x:x[1], reverse=True)
    fit_pop = fit_pop[:5]

    for e in fit_pop:
        elite.append([e[1], pop[e[0]].chromosome, pop[e[0]].mask])
        pop[e[0]].generate_xml_elite(individual = e[0], gen = gen)

    elite.sort(key=lambda x:x[0], reverse=True)
    elite = elite[:max_elite]

    all_fit.append((gen_fit/len(pop)))
    fit_Alen.append((len_fit/len(pop)))
    fit_Amov.append((mov_fit/len(pop)))
    
    # Increase value of the generation for the next cycle
    gen = gen + 1

t_finish = datetime.datetime.now()
print("Total time is: " + str(t_finish-t_begin))
plot(all_fit, '-.b', label='General Fitness')
#plot(fit_Alen, '-g', label='Fitness by pieces')
#plot(fit_Amov, '.r', label='Error by movement')
pylab.legend(loc='center left', bbox_to_anchor=(1, 0.5))
