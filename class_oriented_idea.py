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
from yaspin.yaspin import yaspin
import os
import json
import sys
import subprocess
import itertools
import operator
import shutil
import numpy as np
from copy import deepcopy

# Local files
import XmlHelpers as xml
import Evaluation as Eval 
from Selection import Selection
from Mutation import Mutation

author = "Salinas Hernandez Jaime"
copyright = "Copyright 2018, Tijuana Institute of Technology"
credits = ["Dr. Mario García Valdez",""]
license = "ITT"
version = "1.4.1"
date = "May 08, 2019 18:30"
maintainer = "Salinas Hernandez Jaime"
email = "jaime.salinas@tectijuana.edu.mx"
status = "Development"
t_begin = datetime.datetime.now()
t_prev = datetime.datetime.now()

for pasada in range(1):
    
    
    ## Values used for the genetic algorithm
    population = 10         # For now it can only be below 10
    max_gen = 30            # Max number of generations
    fits = [0]              # Variable to save the fitness of each generation
    gen = 0                 # Generation 1
    per_cross = 0.5         # Percentage of cross-over (cross-over operator)
    per_comb = 0.3          # Percentage of combination (combination operator)
    per_mut = 0.3           # Percentage of mutation
    sel_type = 1            # Selection (for crossover) type [ 0: Random - 1: Tournament - TBD]
    cross_type = 0          # Type of cross-over [ 0: One point CO - 1: Random point CO - TBD]
    ind_pieces = 20         # Number of pieces that define an individual
    all_fit = [0]            # Average fitness for all generations
    all_div = []
    fit_ham = []           # Average piece length fitness for all generations
    fit_Amov = []           # Average movement fitness for all generations
    hamming_global = []
    max_elite = 3           # Maximum number of elite members in the generation
    fit_diversity = 0
    elite = []
    best_gen = []
    mu = 0                  # Mean for normal distribution
    sigma = 20              # SD for normal distribution
    
    min_fit = [0]            # Average fitness for all generations
    max_fit = [0]            # Average fitness for all generations
    
    ## Data required to create the xml files
    
    #####################################################################
    ##############< Data required to create the xml files >##############
    #####################################################################
    
    project_root = os.getcwd()
    json_data = {}
    json_data['all_fit'] = []
    json_data['hamming_avg'] = []
    json_data['min_fit'] = []
    json_data['max_fit'] = []
    json_data['hamming_min'] = []
    ruleset = open("Ruleset/parameters.txt", "r")
    config_param = json.loads(open("ga_parameters.json","r").read())
    
    game_path = config_param['game_path']
    write_path = config_param['write_path']
    elite_path = config_param['elite_path']
    read_path = config_param['read_path']
    log_path = config_param['log_dir']
    log_base_name = config_param['log_base_name']
    child_level = config_param['child_level']
    child_output = config_param['child_output']
    
    # For tournament
    game_path_tourney = config_param['game_path_tourney']
    write_path_tourney = config_param['write_path_tourney']
    read_path_tourney = config_param['read_path_tourney']
    
    # To have a copy of the generations
    level_files_path = config_param['level_files']
    current_gen_folder = config_param['generation']
    sourcefolder = os.path.join(project_root, level_files_path + "/Levels")
    sourcefolder_elite = os.path.join(project_root, level_files_path + "/GenElite")
    experimentsource = os.path.join(project_root, level_files_path)
    foldername = ''.join(e for e in str(datetime.datetime.now()) if e.isalnum())
    experimentdest = config_param['experiment_results'] + "/" + foldername
    experimentdestination = os.path.join(project_root, experimentdest)
    
    # Data for the competition
    req_levels = int(deepcopy(ruleset.readline()))
    req_np_combinations = ruleset.readline().split(',')
    for i, e in enumerate(req_np_combinations):
        req_np_combinations[i] = req_np_combinations[i].split()
    req_pigs = ruleset.readline().split(',')
    
    max_elite = req_levels
    
    # Clean previous experiment
    #shutil.rmtree(os.path.join(project_root, write_path))
    #shutil.rmtree(os.path.join(project_root, elite_path))
    try:
        shutil.rmtree(os.path.join(project_root, level_files_path))
    except:
        print("Folder non-existent")
    
    os.makedirs(os.path.join(project_root, level_files_path), exist_ok=True)
    
    os.makedirs(os.path.join(project_root, write_path), exist_ok=True)
    os.makedirs(os.path.join(project_root, elite_path), exist_ok=True)
    os.makedirs(os.path.join(project_root, read_path), exist_ok=True)
    
    os.makedirs(os.path.join(project_root, log_path), exist_ok=True)
    
    
    
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
        def __init__(self, x, y, r, mat):
            #self.Height = 72
            #self.Width = 72
            self.Material = mat
            self.Dict = []
            self.Valid = True
            self.X = x
            self.Y = y
            self.R = r
            if self.Materials[0] == 0:
                self.Material = "stone"
            if self.Materials[1] == 0:
                self.Material = "ice"
            
        
        def get_edges(self):
            ed_lis = []
            ed_lis.append(deepcopy([self.Width/2 +       self.X,         self.Height/2 +     self.Y]))
            ed_lis.append(deepcopy([self.Width/2 +       self.X, 0 -     self.Height/2 +     self.Y]))
            ed_lis.append(deepcopy([0 - self.Width/2 +   self.X, 0 -     self.Height/2 +     self.Y]))
            ed_lis.append(deepcopy([0 - self.Width/2 +   self.X,         self.Height/2 +     self.Y]))
            self.Edges = ed_lis
    
        def get_points(self, r):
            ang = self.R * pi / 180
            ots = Rotate2D(self.Edges, ar([0 + self.X, 0 + self.Y]), ang)
            self.Points = ots.tolist()
            #print(self.Points)
    
        def change_material(self, m):
            self.Material = m
    
        def as_dictionary(self):
            self_list = []
            self_list.append(deepcopy(self.Name))
            self_list.append(deepcopy(self.Material))
            self_list.append(deepcopy(self.X))
            self_list.append(deepcopy(self.Y))
            self_list.append(deepcopy(self.R))
            self.Dict = self_list
            
        def update_values(self):
            #if 'errormessage' in kwargs:
            #    print("llegue")
            #else: 
            #    self.Material = kwargs.get('material')
            #self.Material = "ice"
            self.get_edges()
            self.get_points(self.R)
            self.as_dictionary()
    
    class Circle(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "Circle"
            self.Height = 75
            self.Width = 75
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    class RectTiny(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "RectTiny"
            self.Height = 25
            self.Width = 45
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
        
    
    class RectSmall(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "RectSmall"
            self.Height = 25
            self.Width = 85
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class RectMedium(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "RectMedium"
            self.Height = 25
            self.Width = 165
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class RectBig(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "RectBig"
            self.Height = 25
            self.Width = 185
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class RectFat(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "RectFat"
            self.Height = 45
            self.Width = 85
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class SquareTiny(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "SquareTiny"
            self.Height = 22
            self.Width = 22
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class SquareSmall(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "SquareSmall"
            self.Height = 45
            self.Width = 45
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class Triangle(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "Triangle"
            self.Height = 75
            self.Width = 75
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class TriangleHole(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "TriangleHole"
            self.Height = 85
            self.Width = 85
            Piece.__init__(self, x, y, r, mat)
            self.update_values()
    
    
    class SquareHole(Piece):
        def __init__(self, mat, x=0, y=0, r=0):
            self.Name = "SquareHole"
            self.Height = 85
            self.Width = 85
            Piece.__init__(self, x, y, r, mat)
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
            self.Objetos = [clases[clase](m,x,y,r) for (clase,x,y,r,m) in self.blocks.copy()]
            self.get_values()
            self.height = self.height()
            self.width = self.width()
            self.top_center = self.gen_top_center()
            self.as_dictionary = self.gen_dictionary()
            self.low_center = self.get_low_center()
            self.overtop_center = self.get_overtop()
            
        def get_values(self):
            if len(self.blocks) > 2:
                self.Pig = True
            else:
                self.Pig = False
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
    
        def gen_top_center(self):
            height_center = self.Height/2
            lenght_center = 0
            return [lenght_center, height_center]
        
        def get_low_center(self):
            return [0, self.Height/2]
        
        def get_overtop(self):
            return [0, self.Height]
    
        def gen_dictionary(self):
            block_list = []
            block_list.append(deepcopy([self.Width, self.Height])) # Width represents the x coordinate and Height the y one
            for piece in self.Objetos:
                block_comp = []
                block_comp.append(deepcopy(piece.Dict[0]))
                block_comp.append(deepcopy(piece.Dict[1]))
                block_comp.append(deepcopy(piece.Dict[2]))
                block_comp.append(deepcopy(piece.Dict[3]))
                block_comp.append(deepcopy(piece.Dict[4]))
                block_list.append(deepcopy(block_comp))
            #block_list.append(block_comp)
            #print(block_list)
            return block_list
        
        def move_xy(self, n_x, n_y, mat_f, el_r):
            #self.X = n_x
            #self.Y = n_y
            self.Objetos = [clases[clase](mat_f, x + n_x, y + n_y, el_r) for (clase,x,y,r, mat) in self.blocks.copy()]
            return 0
        
        def as_json(self):
            return {}
        
        def set_number(self, num):
            self.Composite_number = deepcopy(num)
            pass
       
    
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
    Composites = {
        0: [("RectBig", 0, -91, 0, "wood"), ("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")],
        1: [("RectBig", 0, -31, 0, "wood"), ("RectTiny", -90, 0, 90, "wood"), ("RectTiny", 90, 0, 90, "wood"), ("RectBig", 0, 31, 0, "wood")],
        2: [("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")],
        3: [("RectMedium", 0, 0, 90, "wood"), ("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")],
        4: [("RectBig", 100, 5, -27, "wood"), ("RectBig", -100, 5, 27, "wood"), ("RectSmall", 0, 0, 90, "wood")]#,
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
    
    Composites = {
        0: [("RectTiny", 0, 0, 0, "wood")],
        1: [("RectSmall", 0, 0, 0, "wood")],
        2: [("RectMedium", 0, 0, 0, "wood")],
        3: [("RectBig", 0, 0, 0, "wood")],
        4: [("RectFat", 0, 0, 0, "wood")],
        5: [("SquareSmall", 0, 0, 0, "wood")],
        6: [("SquareHole", 0, 0, 0, "wood")],
        7: [("Circle", 0, 0, 0, "wood")],
        8: [("TriangleHole", 0, 0, 0, "wood")],
        9: [("RectBig", 0, -91, 0, "wood"), ("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")],
        10: [("RectBig", 0, -31, 0, "wood"), ("RectTiny", -90, 0, 90, "wood"), ("RectTiny", 90, 0, 90, "wood"), ("RectBig", 0, 31, 0, "wood")]
    }
    
    Composites_res = {
        0: [("RectTiny", 0, 0, 0, "wood", True)],
        1: [("RectSmall", 0, 0, 0, "wood", True)],
        2: [("RectMedium", 0, 0, 0, "wood", True)],
        3: [("RectBig", 0, 0, 0, "wood", True)],
        4: [("RectFat", 0, 0, 0, "wood", True)],
        5: [("SquareSmall", 0, 0, 0, "wood", True)],
        6: [("SquareHole", 0, 0, 0, "wood", True)],
        7: [("Circle", 0, 0, 0, "wood", True)],
        8: [("TriangleHole", 0, 0, 0, "wood", True)]
    }
    
    materials = {
            "wood": 0,
            "stone": 1,
            "ice": 2}
    
    restrictions = {
            "Circle": [1,1,1],
            "CircleSmall": [1,1,1],
            "RectTiny": [1,1,1],
            "RectSmall": [1,1,1],
            "RectMedium": [1,1,1],
            "RectBig": [1,1,1],
            "RectFat": [1,1,1],
            "SquareTiny": [1,1,1],
            "SquareSmall": [1,1,1],
            "SquareHole": [1,1,1],
            "Triangle": [1,1,1],
            "TriangleHole": [1,1,1] }
    
    for element in req_np_combinations:
        restrictions[element[1]][materials[element[0]]] = 0
        
    for piece in Composites_res:
        clases[Composites_res[piece][0][0]].Materials = restrictions[Composites_res[piece][0][0]]
        
    for piece in Composites_res:
        if sum(clases[Composites_res[piece][0][0]].Materials) == 0:
            clases[Composites_res[piece][0][0]].Valid = False
        else:
            clases[Composites_res[piece][0][0]].Valid = True
            #if clases[Composites_res[piece][0][0]].Materials[0] == 0:
                
        #if sum(piece.Materials) == 0:
            #piece.Valid = False
    def get_random_chrom(sl):
        asl = 0
        chrom = []
        while asl < sl:
            prop = random.randint(0, len(Composites)-1)
            if clases[Composites[prop][0][0]].Valid == True:
                chrom.append(deepcopy(prop))
                asl += 1
        #random.randint(0,len(Composites)-1) for p in range(ind_pieces)
        return chrom
    
    def combine_pieces():
        """
        a = [("RectBig", 0, -91, 0, "wood"), ("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")]
        b = [("RectBig", 0, -31, 0, "wood"), ("RectTiny", -90, 0, 90, "wood"), ("RectTiny", 90, 0, 90, "wood"), ("RectBig", 0, 31, 0, "wood")]
        c = [("RectBig", 100, 5, -27, "wood"), ("RectBig", -100, 5, 27, "wood"), ("RectSmall", 0, 0, 90, "wood")]
        d = [("RectBig", 100, 5, -27, "wood"), ("RectSmall", 0, 0, 90, "wood")]
        e = [("RectBig", -100, 5, 27, "wood"), ("RectSmall", 0, 0, 90, "wood")]
        f = [("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")]
        g = [("RectMedium", 0, 0, 90, "wood"), ("RectMedium", -90, 0, 90, "wood"), ("RectMedium", 90, 0, 90, "wood"), ("RectBig", 0, 91, 0, "wood")]
        grupo = [a,b,c,d,e,f,g]
        piece1 = random.randint(0, len(Composites)-1)
        piece2 = random.randint(0, len(Composites)-1)
        for c in grupo:    
            new_value = len(Composites)
            Composites.update({deepcopy(new_value):deepcopy(c)})
        """
        piece1 = random.randint(0, len(Composites)-1)
        piece2 = random.randint(0, len(Composites)-1)
        new_value = len(Composites)
        prop1 = Composite(Composites[piece1])
        prop2 = Composite(Composites[piece2])
        final_group = []
        if piece1 == piece2:
            initial = random.randint(0,1)
            if initial == 0: # Estaran pegados
                # Checar si los bordes coinciden
                #print("Igual pegados")
                prop1.move_xy(prop1.Width/2,0,prop1.Objetos[0].Material, 0)
                prop2.move_xy((0-(prop2.Width/2)),0,prop2.Objetos[0].Material, 0)
                prop1.get_values()
                prop2.get_values()
                list1 = prop1.Borders
                list2 = prop2.Borders
                # Calculate center point of each piece and add to list
                test=Composites[piece1].copy()
                for comp in test:
                    temp = []
                    temp.append(comp[0])
                    temp.append(int(comp[1]) + (prop1.Width/2))
                    temp.append(int(comp[2]))
                    temp.append(int(comp[3]))
                    temp.append(comp[4])
                    fin = tuple(temp)
                    final_group.append(fin)
                test = Composites[piece2].copy()
                for comp in test:
                    temp = []
                    temp.append(comp[0])
                    temp.append(int(comp[1]) - (prop2.Width/2))
                    temp.append(int(comp[2]))
                    temp.append(int(comp[3]))
                    temp.append(comp[4])
                    fin = tuple(temp)
                    final_group.append(deepcopy(fin))
            else:
                mov_rand = random.randint(math.ceil(prop1.Width/2),90)
                #print("Igual separados")
                prop1.move_xy((prop1.Width/2) + mov_rand,0,prop1.Objetos[0].Material, 0)
                prop2.move_xy((0-((prop2.Width/2) + mov_rand)),0,prop2.Objetos[0].Material, 0)
    
                prop1.get_values()
                prop2.get_values()
                prop3 = Composite(Composites[3])
                
                prop3.move_xy(0,(prop1.Height/2)+(prop3.Height/2), prop3.Objetos[0].Material, 0)
                prop3.get_values()
    
                points = [[(prop1.Width/2) + mov_rand,0], [(0-((prop2.Width/2) + mov_rand)),0], [0,(prop1.Height/2)+(prop3.Height/2)]]
                com = np.mean(points, axis=0)
                delta = np.array((0,0)) - com
                shifted_points = points + delta
    
                list1 = prop1.Borders
                list2 = prop2.Borders
                list3 = prop3.Borders
                #final_group.extend(Composites[piece1])
                #final_group.extend(Composites[piece2])
                #final_group.extend(Composites[3])
                #print(list3)
                test=Composites[3].copy()
                for comp in test:
                    temp = []
                    temp.append(comp[0])
                    #temp.append(int(comp[1]))
                    #temp.append(int(comp[2]) + (prop1.Height/2)+(prop3.Height/2) + 1)
                    temp.append(shifted_points[2][0])
                    temp.append(shifted_points[2][1]+1)
                    temp.append(int(comp[3]))
                    temp.append(comp[4])
                    fin = tuple(temp)
                    final_group.append(deepcopy(fin))
                test = Composites[piece1].copy()
                for comp in test:
                    temp = []
                    temp.append(comp[0])
                    #temp.append(int(comp[1]) + (prop1.Width/2) + mov_rand + 1)
                    #temp.append(int(comp[2]))
                    temp.append(shifted_points[0][0])
                    temp.append(shifted_points[0][1])
                    temp.append(int(comp[3]))
                    temp.append(comp[4])
                    fin = tuple(temp)
                    final_group.append(deepcopy(fin))
                test = Composites[piece2].copy()
                for comp in test:
                    temp = []
                    temp.append(comp[0])
                    #temp.append(int(comp[1]) + (0-((prop2.Width/2) + mov_rand)) - 1)
                    #temp.append(int(comp[2]))
                    temp.append(shifted_points[1][0])
                    temp.append(shifted_points[1][1])
                    temp.append(int(comp[3]))
                    temp.append(comp[4])
                    fin = tuple(temp)
                    final_group.append(deepcopy(fin))
            Composites.update({new_value:deepcopy(final_group)})
        else:
            #print("Diferente pegados")
            ap1 = prop1.Width*prop1.Height
            ap2 = prop2.Width*prop2.Height
            if ap1 > ap2:
                if prop1.Width >= 90:
                    #print("Vertical")
                    prop1.Objetos[0].R = 90
                    prop1.Objetos[0].update_values()
                    prop1.move_xy(0,(0-(prop1.Width/2)),prop1.Objetos[0].Material, 90)
    
                    prop2.move_xy(0,(prop2.Height/2),prop2.Objetos[0].Material, 0)
    
                    points = [[0,(0-(prop1.Width/2))], [0,(prop2.Height/2)]]
                    com = np.mean(points, axis=0)
                    delta = np.array((0,0)) - com
                    shifted_points = points + delta
                    test = Composites[piece1].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[2]) + (prop1.Width/2))
                        temp.append(shifted_points[0][0])
                        temp.append(shifted_points[0][1]-1)
                        temp.append(90)
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                    test = Composites[piece1].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]) + (0-((prop2.Width/2))) - 1)
                        temp.append(shifted_points[1][0])
                        temp.append(shifted_points[1][1]+1)
                        #temp.append(int(comp[2]))
                        temp.append(int(comp[3]))
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                else:
                    #print("Horizontal")
                    prop1.move_xy((0-(prop1.Width/2)),0,prop1.Objetos[0].Material, 0)
                    prop2.move_xy((prop2.Width/2),0,prop2.Objetos[0].Material, 0)
                    points = [[0,(0-(prop1.Width/2))], [0,(prop2.Width/2)]]
                    com = np.mean(points, axis=0)
                    delta = np.array((0,0)) - com
                    shifted_points = points + delta
                    test = Composites[piece1].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]))
                        #temp.append(int(comp[2]) + (prop1.Width/2))
                        temp.append(shifted_points[0][0])
                        temp.append(shifted_points[0][1])
                        temp.append(int(comp[3]))
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                    test = Composites[piece2].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]) + (0-((prop2.Width/2))) - 1)
                        temp.append(shifted_points[1][0])
                        temp.append(shifted_points[1][1])
                        #temp.append(int(comp[2]))
                        temp.append(int(comp[3]))
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
            else:
                if prop2.Width >= 90:
                    #print("Vertical")
                    prop2.Objetos[0].R = 90
                    prop2.Objetos[0].update_values()
                    prop2.move_xy(0,(0-(prop2.Width/2)),prop2.Objetos[0].Material, 90)
                    prop1.move_xy(0,(prop1.Height/2),prop1.Objetos[0].Material, 0)
                    points = [[0,(0-(prop2.Width/2))], [0,(prop1.Height/2)]]
                    com = np.mean(points, axis=0)
                    delta = np.array((0,0)) - com
                    shifted_points = points + delta
                    test = Composites[piece1].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]))
                        #temp.append(int(comp[2]) + (prop1.Width/2))
                        temp.append(shifted_points[0][0])
                        temp.append(shifted_points[0][1]+1)
                        temp.append(int(comp[3]))
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                    test = Composites[piece2].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]) + (0-((prop2.Width/2))) - 1)
                        temp.append(shifted_points[1][0])
                        temp.append(shifted_points[1][1]-1)
                        #temp.append(int(comp[2]))
                        temp.append(90)
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                else:
                    #print("Horizontal")
                    prop2.move_xy((0-(prop2.Width/2)),0,prop2.Objetos[0].Material, 0)
                    prop1.move_xy((prop1.Width/2),0,prop1.Objetos[0].Material, 0)
                    points = [[0,(0-(prop2.Width/2))], [0,(prop1.Width/2)]]
                    com = np.mean(points, axis=0)
                    delta = np.array((0,0)) - com
                    shifted_points = points + delta
                    test = Composites[piece1].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]))
                        #temp.append(int(comp[2]) + (prop1.Width/2))
                        temp.append(shifted_points[0][0])
                        temp.append(shifted_points[0][1])
                        temp.append(int(comp[3]))
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                    test = Composites[piece2].copy()
                    for comp in test:
                        temp = []
                        temp.append(comp[0])
                        #temp.append(int(comp[1]) + (0-((prop2.Width/2))) - 1)
                        temp.append(shifted_points[1][0])
                        temp.append(shifted_points[1][1])
                        #temp.append(int(comp[2]))
                        temp.append(int(comp[3]))
                        temp.append(comp[4])
                        fin = tuple(temp)
                        final_group.append(deepcopy(fin))
                #prop1.move_xy(0,(prop1.Height/2),prop1.Objetos[0].Material, 0)
                #prop2.move_xy(0,(0-(prop2.Height/2)),prop2.Objetos[0].Material, 0)
            Composites.update({new_value:deepcopy(final_group)})
            prop1.get_values()
            prop2.get_values()
            list1 = prop1.Borders
            list2 = prop2.Borders
    
        #print(list1)
        #print(list2)
        
    
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
    sel_operator = Selection(project_root, game_path_tourney, info)
    mut_operator = Mutation(per_mut, mu, sigma, clases)
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
            self.Mut_Material = ["wood" for value in self.chromosome]
    
        def position_chromosome(self):
            #To do
            # Here you can use the chromosome objects etc.
            pass
        
        def UpdateMutation(self):
            for c, struc in enumerate(self.Mut_Struct):
                if struc != -1:
                    self.chromosome[c] = deepcopy(struc)
    
            self.chromosome_objects = [Composite(Composites[composite]) for composite in self.chromosome]
    
            for c, objeto in enumerate(self.chromosome_objects):
                for pieza in objeto.Objetos:
                    if self.Mut_Material[c] != 0:
                        pieza.Material = deepcopy(self.Mut_Material[c])
                        pieza.change_material(self.Mut_Material[c])
                        pieza.update_values()
                objeto.as_dictionary = deepcopy(objeto.gen_dictionary())
            """ 
            for mat in self.Mut_Material:
                for objeto in self.chromosome_objects:
                    for pieza in objeto.Objetos:
                        if mat != 0:
                            pieza.Material = mat
                            pieza.update_values()
            """
            for c, mov in enumerate(self.Mut_Movement):
                self.chromosome_objects[c].move_xy(mov, 0, self.Mut_Material[c], 0)
    
            self.object_list = deepcopy(self.object_list_gen())
            pass
        
        def chromosome_coordinates(self):
            
            return [0, 0]
        
        def object_list_gen(self):
            final_list = []
            for com in self.chromosome_objects:
                com.as_dictionary = deepcopy(com.gen_dictionary())
                obj_list =[]
                obj_list.append(deepcopy(com.as_dictionary))
                final_list.append(deepcopy(obj_list))
            return final_list
        
        def generate_xml(self, **kwargs):
            res_list = []
            res_list = deepcopy(xml.writeXML(self.object_list, os.path.join(project_root, write_path + "/level-0"+ str(kwargs.get('individual')) +".xml")))
            self.ind_height = deepcopy(res_list[0])
            self.ind_piece = deepcopy(res_list[1])
            self.Pieces = deepcopy(res_list[2])
            self.eliminate_repeated()
            pass
        
        def eliminate_repeated(self):
            current = None
            eliminate = []
            counter = 0
            for piece in self.Pieces:
                if piece[5] != current:
                    current = deepcopy(piece[5])
                else:
                    eliminate.append(deepcopy(counter))
                counter += 1
        
            # Then eliminate the repeated values
            temp_pieces = deepcopy(self.Pieces)
            temp_pieces = deepcopy(temp_pieces[:(int(current))])
            self.Pieces = deepcopy(temp_pieces)
            
        
        def read_xml(self, **kwargs):
            self.Remaining_Pieces = deepcopy(xml.readXML(os.path.join(project_root, read_path + "/level-"+ str(kwargs.get('individual')) +".xml")))
            self.ind_piece_count = len(self.Remaining_Pieces)
            pass
        
        def read_xml_tourney(self, **kwargs):
            self.Remaining_Pieces = deepcopy(xml.readXML(os.path.join(project_root, read_path_tourney + "/level-"+ str(kwargs.get('individual')) +".xml")))
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
    
        def locate_pigs(self):
            self.Pig_Location = mut_operator.Set_Pigs(self.chromosome_objects, req_pigs, self.mask, self.Composites_Centers)
            pass
        
        def get_fitness(self, chrom_list, pos):
            temp_list = []
            self.Fitness, temp_list, self.Fit_Pos = deepcopy(Eval.fitness(self.Pieces, self.Remaining_Pieces, self.chromosome, chrom_list, pos))
            self.Diversity = deepcopy(temp_list[0])
            self.Fitness = deepcopy(self.Diversity)
            self.Fit_Hamming = deepcopy(temp_list[1])
            #self.Fitness, self.Fit_Hamming, self.Fit_Pos = Eval.fitness(self.Pieces, self.Remaining_Pieces, self.chromosome, chrom_list, pos)
            return 0
        
        def combine_mask(self):
            self.object_masked, self.Composites_Centers, self.Mask_Control = deepcopy(xml.calculate_mask(self.object_list, self.mask, self.chromosome_objects, self.chromosome))
            #self.object_list = xml.calculate_mask(self.object_list, type_castle)
            return 0
        def generate_xml_masked(self, **kwargs):
            res_list = []
            res_list = xml.writeXML_masked(self.Pig_Location, self.object_list, os.path.join(project_root, write_path + "/level-0"+ str(kwargs.get('individual')) +".xml"))
            self.ind_height = res_list[0]
            self.ind_piece = res_list[1]
            self.Pieces = res_list[2]
            self.eliminate_repeated()
            #print("XML Completo")
            pass
        
        def generate_xml_tourney(self, **kwargs):
            res_list = []
            res_list = xml.writeXML_masked(self.Pig_Location, self.object_list, os.path.join(project_root, write_path_tourney + "/level-0"+ str(kwargs.get('individual')) +".xml"))
            self.ind_height_tourney = res_list[0]
            self.ind_piece_tourney = res_list[1]
            self.Pieces = res_list[2]
            self.eliminate_repeated()
            pass
    
        def generate_xml_elite(self, **kwargs):
            res_list = []
            res_list = xml.writeXML_masked(self.Pig_Location, self.object_list, os.path.join(project_root, elite_path + "/level-" + str(kwargs.get('gen')) + "0" + str(kwargs.get('individual'))  + ".xml"))
            self.ind_height = res_list[0]
            self.ind_piece = res_list[1]
            self.Pieces = res_list[2]
            self.eliminate_repeated()
            pass
        
    
    def create_new_mask(pieces):
        div_list =[]
        while True:
            div_list = [random.randint(0, pieces-1) for col in range(7)]
            if sum(div_list) == pieces:
                break
        
        return div_list
    
    # Generate a defined number of new composites to add to the pool of selections
    for i in range(0,9):
        try:
            combine_pieces()
        except:
            print("Error generating composites")
        
    #combine_pieces()
    #pop_mask = [random.randint(0,len(Mask_List)-1) for i in range(population)]
    #pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)], mask = Mask_List[random.randint(0,len(Mask_List)-1)]) for i in range(population)]
    
    #pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)], mask = create_new_mask(ind_pieces)) for i in range(population)]
    pop = [ Individual(chromosome = get_random_chrom(ind_pieces), mask = create_new_mask(ind_pieces)) for i in range(population)]
    # variable for controlling that the fitness of the population is compared to at least 2 others in the same timeline (between resets)
    gen_alive = 0
    #for c, ind in enumerate(pop):
    #    ind.assign_mask(mask=pop_mask[c])
    """
    for ind in pop:
        for gen in ind.chromosome_objects:
            #print(gen.blocks)
            #print('')
            pass
    """    
    
    
    with yaspin(text="Executing algorithm", color="cyan") as sp: 
        while gen < max_gen: #and max(fits) < 100:
            #fits = [0]
            # If the current generation is not the first one generate a new population
            ###if gen != 1:
            #    Determine via a random number which pieces to assign
            #   pop = [ Individual(chromosome = [random.randint(0,len(Composites)-1) for p in range(ind_pieces)]) for i in range(population)]
            ###
                    
            # Outside IF statement
            # Reintegrate the ELITE member to the population and remove the one in the last possition
            if len(elite):
                for member in elite:
                    pop.insert(0, deepcopy(member))
                    #pop[0] = Individual(chromosome = member[1], mask = member[2])
                    pop = pop[:population]
    
            # Check if the current number of population multiplied by the cross-over percentage
            # is an even or odd number, in the later case remove 1 from the value
            many = len(pop) * per_cross
            if many % 2 == 0:
                pass
            else:
                many = many - 1
    
            # Combine the mask of the individual before entering the simulation
            ind_c = 0
            for ind in pop:
                if hasattr(ind, 'Fitness'):
                    pass
                else:
                    ind.combine_mask()
                    ind.locate_pigs()
                ind.generate_xml_masked(individual = deepcopy(ind_c))
                ind_c = ind_c + 1
            
            # Runs and instance of the game
            #subprocess.Popen(r'"' + os.path.join(project_root, game_path) + '"', startupinfo=info)  # doesn't capture output
            if hasattr(ind, 'Fitness'):
                pass
            else:
                subprocess.call(r'"' + os.path.join(project_root, game_path) + '"', startupinfo=info)  # doesn't capture output
    
            # After the simulation obtain the fitness value for the population
            # Read the xml files and get the data
            if hasattr(ind, 'Fitness'):
                pass
            else:
                ind_c = 0
                final_ind_list = []
                for ind in pop:
                    value = ind.read_xml(individual = deepcopy(ind_c))
                    final_ind_list.append(deepcopy(value))
                    ind_c = ind_c + 1
    
            # Generate a list with the chromosome values of all individuals (required for Hamming distance)
            chrom_list = []
            for ind in pop:
                chrom_list.append(deepcopy(ind.chromosome))
    
            # Calculate the fitness for each individual
            for c, ind in enumerate(pop):
                ind.get_fitness(chrom_list, c)
                pass
    
            ############################################################################
            #############################< Selection steps >############################
            ############################################################################ 
            
            # Order the population by their fitness
            #pop.sort(key=lambda x:x.Fitness, reverse=False)
    
            # Obtain the "parents" of the generation
            parents = []
            pr = 1
            parents = sel_operator.Selection_Base(pop, many, sel_type)
    
            ############################################################################
            #############################< Crossover steps >############################
            ############################################################################
            
            new_members = []
    
            # Generate the cross-over operation (one-point crossover)
            pos_offspring = 0
            for cross_parent in range(0, len(parents), 2):
                pos_offsping = len(pop)
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
                
                mask_son = create_new_mask(len(son))
                mask_daughter = create_new_mask(len(daughter))
                # Replace the parents in the generation
                #pop[pos_offspring].chromosome = son
                #pop[pos_offspring + 1].chromosome = daughter
                pop[parents[cross_parent]] = deepcopy(Individual(chromosome = son, mask = mask_son))
                pop[parents[cross_parent + 1]] = deepcopy(Individual(chromosome = daughter, mask = mask_daughter))
                
                #pop.append(deepcopy(Individual(chromosome = son, mask = mask_son)))
                #pop.append(deepcopy(Individual(chromosome = daughter, mask = mask_daughter)))
    
                # Mutate the childs (by chance like throwing a 100 side dice)
                # If greater than the treshold then mutate
                chance = random.randint(1, 100)
                threshold = 100 - (100 * per_mut)
                #chance = 100
                if chance > threshold:
                    var=0
                    new_chrom = mut_operator.M_Individual(pop[parents[cross_parent]].chromosome)
                    pop[parents[cross_parent]] = deepcopy(Individual(chromosome = deepcopy(new_chrom), mask = create_new_mask(len(new_chrom))))
                    #pop[parents[cross_parent]] = deepcopy(mut_operator.M_Movement(pop[parents[cross_parent]], 0))
                    pop[parents[cross_parent]] = deepcopy(mut_operator.M_StrucType(pop[parents[cross_parent]], 0))
                    pop[parents[cross_parent]] = deepcopy(mut_operator.M_StructMat(pop[parents[cross_parent]], 0))
                    pop[parents[cross_parent]].UpdateMutation()
                    #print("Mutate")
                else:
                    var=1
                    #print("Not Mutate")
                
                # The same for the second child
                chance = random.randint(1, 100)
                threshold = 100 - (100 * per_mut)
                #chance = 100
                if chance > threshold:
                    var=0
                    new_chrom = mut_operator.M_Individual(pop[-1].chromosome)
                    pop[parents[cross_parent + 1]] = deepcopy(Individual(chromosome = deepcopy(new_chrom), mask = create_new_mask(len(new_chrom))))
                    #pop[parents[cross_parent + 1]] = deepcopy(mut_operator.M_Movement(pop[parents[cross_parent + 1]], 0))
                    pop[parents[cross_parent + 1]] = deepcopy(mut_operator.M_StrucType(pop[parents[cross_parent + 1]], 0))
                    pop[parents[cross_parent + 1]] = deepcopy(mut_operator.M_StructMat(pop[-1], 0))
                    pop[parents[cross_parent + 1]].UpdateMutation()
                    #print("Mutate")
                
                pop[parents[cross_parent]].ind_c = deepcopy(parents[cross_parent])
                pop[parents[cross_parent + 1]].ind_c = deepcopy(parents[cross_parent + 1])
                new_members.append(pop[parents[cross_parent]])
                new_members.append(pop[parents[cross_parent + 1]])
            
            # Calculate the new individuals fitness by sending them to a diferent simulation track
            
            # Generate an XML to check the fitness
            for ind_c, ind in enumerate(new_members):
                ind.combine_mask()
                ind.locate_pigs()
                ind.generate_xml_tourney(individual = ind_c)
            
            # Execute the application with the two memebers
            subprocess.call(r'"' + os.path.join(project_root, game_path_tourney) + '"', startupinfo=info)
    
            # Generate a list with the chromosome values of all individuals (required for Hamming distance)
            chrom_list = []
            for ind in pop:
                chrom_list.append(deepcopy(ind.chromosome))
    
            # Then obtain the remaining fitness values
            for c, ind in enumerate(new_members):
                ind.read_xml_tourney(individual = c)
                ind.get_fitness(chrom_list, c)
    
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
            hamming_fit = 0
            mov_fit = 0
            best_ind = 0
            fit_diversity = 0
            fit_pop = []
            ham_gen_list = []
            for c, ind in enumerate(pop):
                fit_pop.append([deepcopy(c), deepcopy(ind.Fitness)])
                gen_fit = deepcopy(gen_fit + ind.Fitness)
                #if c == 0:
                #    best_gen.append(ind.Fitness)
                hamming_fit += deepcopy(ind.Fit_Hamming)
                fit_diversity += deepcopy(int(ind.Diversity))
                mov_fit += deepcopy(ind.Fit_Pos)
                ham_gen_list.append(deepcopy(ind.Fit_Hamming))
            
            fit_pop.sort(key=lambda x:x[1], reverse=True)
            #max_fit.append(fit_pop[0][1])
            min_fit.append(deepcopy(fit_pop[-1][1]))
            #fit_pop = deepcopy(fit_pop[:5])
            ham_gen_list.sort(key=lambda x:x, reverse=False)
            hamming_global.append(deepcopy(ham_gen_list[0]))
            # 
            best_gen.append(deepcopy(fit_pop[0][1]))
            
            # Add the worst value to a history list
            #if len(min_fit) == 1:
            #    min_fit.append(deepcopy(fit_pop[-1][1]))
            #elif min_fit[-1] >= fit_pop[-1][1]:
            #    min_fit.append(deepcopy(fit_pop[-1][1]))
            #else:
            #    min_fit.append(deepcopy(min_fit[-1]))
    
            # Add the best value to the elite list
            if len(elite) == 0:
                elite.append(deepcopy(pop[fit_pop[0][0]]))
                max_fit.append(deepcopy(elite[0].Fitness))
            elif pop[fit_pop[0][0]].Fitness >= elite[0].Fitness:
                #elite.pop(0)
                elite.append(deepcopy(pop[fit_pop[0][0]]))
                max_fit.append(deepcopy(elite[-1].Fitness))
            else:
                max_fit.append(deepcopy(elite[0].Fitness))
            
            elite.sort(key=lambda x:x.Fitness, reverse=True)
            elite = deepcopy(elite[:max_elite])
            #for e in elite:
            #    elite.append(pop[e[0]])
            #    elite[0].generate_xml_elite(individual = e[0], gen = gen)
                #elite.append([e[1], pop[e[0]].chromosome, pop[e[0]].mask])
                #pop[e[0]].generate_xml_elite(individual = e[0], gen = gen)
    
            #elite.sort(key=lambda x:x.Fitness, reverse=True)
            #elite = elite[:max_elite]
            counter = 0
            for member in elite:
                member.generate_xml_elite(individual = deepcopy(counter), gen = deepcopy(gen))
                counter += 1
    
            all_fit.append(deepcopy(gen_fit/len(pop)))
            fit_ham.append(deepcopy(hamming_fit/len(pop)))
            fit_Amov.append(deepcopy(mov_fit/len(pop)))
            all_div.append(deepcopy(fit_diversity/len(pop)))
            """
            # Check if the 2 generations before were better, if so reset the population
            if gen_alive >= 3:
                if all_fit[gen] <= all_fit[gen-1] and all_fit[gen] <= all_fit[gen-2] and all_fit[gen] <= all_fit[gen-3]:
                    pop = [ Individual(chromosome = get_random_chrom(ind_pieces), mask = create_new_mask(ind_pieces)) for i in range(population)]
                    sp.write("> Restarted population at gen " + str(gen))
                    # Generate the new values of fitness and then order them
    
                    # Combine the mask of the individual before entering the simulation
                    ind_c = 0
                    for ind in pop:
                        ind.combine_mask()
                        ind.locate_pigs()
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
    
                    # Generate a list with the chromosome values of all individuals (required for Hamming distance)
                    chrom_list = []
                    for ind in pop:
                        chrom_list.append(ind.chromosome)
    
                    # Calculate the fitness for each individual
                    for c, ind in enumerate(pop):
                        ind.get_fitness(chrom_list, c)
                        pass
    
                    ############################################################################
                    #############################< Selection steps >############################
                    ############################################################################ 
                    
                    # Order the population by their fitness
                    pop.sort(key=lambda x:x.Fitness, reverse=False)
    
                    # Reset the generation controll
                    gen_alive = 0
            """
            # Increase value of the generation for the next cycle
            gen = gen + 1
            gen_alive += 1
    
            # Print the time of the generation
            t_gen = datetime.datetime.now()
            sp.write("> Gen " + str(gen) + " complete, gen duration: "+ str(t_gen-t_prev) + ", current time: " + str(t_gen-t_begin))
            t_prev = datetime.datetime.now()
            #print("Gen " + str(gen) + " end time: " + str(t_gen-t_begin))
    
            # Copy the resulting files to a folder with the number of generation
            destination = os.path.join(project_root, level_files_path + "/generation-" + str(current_gen_folder))
            #destination = "generation-" + str(current_gen_folder)
            shutil.copytree(sourcefolder, destination)
            
            shutil.rmtree(os.path.join(project_root, write_path))
            #shutil.rmtree(os.path.join(project_root, elite_path))
            shutil.rmtree(os.path.join(project_root, read_path))
    
            #os.makedirs(os.path.join(project_root, level_files_path), exist_ok=True)
            
            os.makedirs(os.path.join(project_root, write_path), exist_ok=True)
            #os.makedirs(os.path.join(project_root, elite_path), exist_ok=True)
            os.makedirs(os.path.join(project_root, read_path), exist_ok=True)
            
            shutil.rmtree(os.path.join(project_root, write_path_tourney))
            shutil.rmtree(os.path.join(project_root, read_path_tourney))
            
            os.makedirs(os.path.join(project_root, write_path_tourney), exist_ok=True)
            os.makedirs(os.path.join(project_root, read_path_tourney), exist_ok=True)
            
            os.makedirs(os.path.join(project_root, log_path), exist_ok=True)
            current_gen_folder += 1
    
        t_finish = datetime.datetime.now()
        #print("Total time is: " + str(t_finish-t_begin))
        sp.write("> Total time is: " + str(t_finish-t_begin))
    
        # Stop the spinner
        sp.ok("✔")
        
    # Plot the results for Fitness
    pylab.figure(figsize=(8, 5))
    plot(all_fit, '-.b', label='General Fitness')
    plot(min_fit, '-g', label='Min fitness value')
    plot(max_fit, '*-r', label='Max fitness value')
    #plot(fit_ham, '-g', label='Average Hamming Distance')
    #plot(fit_Amov, '.r', label='Error by movement')
    lgd = pylab.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    #pylab.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pylab.savefig('Fitness', bbox_extra_artists=(lgd,), bbox_inches='tight')
    pylab.close()
    
    # Same for Hamming Distance
    pylab.figure(figsize=(8, 5))
    plot(fit_ham, '-g', label='Average Hamming Distance')
    lgd = pylab.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pylab.savefig('Hamming', bbox_extra_artists=(lgd,), bbox_inches='tight')
    pylab.close()
    
    pylab.figure(figsize=(8, 5))
    plot(hamming_global, '-g', label='Min Hamming Distance')
    lgd = pylab.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    pylab.savefig('Hamming_Min', bbox_extra_artists=(lgd,), bbox_inches='tight')
    pylab.close()
    
    # Add the data to the json files
    json_data['all_fit'] = deepcopy(all_fit)
    json_data['hamming_avg'] = deepcopy(fit_ham)
    json_data['min_fit'] = deepcopy(min_fit)
    json_data['max_fit'] = deepcopy(max_fit)
    json_data['hamming_min'] = deepcopy(hamming_global)
    
    with open('results.json','w') as outfile:
        print(outfile)
        json.dump(json_data, outfile)
    
    # Clean the workspace
    shutil.copytree(experimentsource, experimentdestination)
    
    shutil.copyfile('results.json',os.path.join(project_root, experimentdest) + '/results.json')
    shutil.copyfile('Fitness.png',os.path.join(project_root, experimentdest) + '/Fitness.png')
    shutil.copyfile('Hamming.png',os.path.join(project_root, experimentdest) + '/Hamming.png')
    shutil.copyfile('Hamming_Min.png',os.path.join(project_root, experimentdest) + '/Hamming_Min.png')