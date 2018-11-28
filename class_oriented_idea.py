from __future__ import division                 #to avoid integer devision problem
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
import XmlHelpers as xml
#--import AngryBirdsGA.XmlHelpers_mod as xml

author = "Salinas Hernandez Jaime"
copyright = "Copyright 2018, Tijuana Institute of Technology"
credits = ["Dr. Mario García Valdez",""]
license = "ITT"
version = "1.0.3"
date = "October 29, 2018 12:38"
maintainer = "Salinas Hernandez Jaime"
email = "jaime.salinas@tectijuana.edu.mx"
status = "Development"



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


class Piece:
    def __init__(self, x, y, r):
        self.Height = 72
        self.Width = 72
        self.Material = "wood"
        self.Dict = []
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.Height/2 +   self.Y,     self.Width/2 + self.X])
        ed_lis.append([0 -  self.Height/2 +   self.Y,     self.Width/2 + self.X])
        ed_lis.append([0 -  self.Height/2 +  self.Y, 0 - self.Width/2 + self.X])
        ed_lis.append([     self.Height/2 +   self.Y, 0 - self.Width/2 + self.X])
        self.Edges = ed_lis

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.Edges, ar([0, 0]), ang)
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
        self.Height = 72
        self.Width = 72
        Piece.__init__(self, x, y, r)
        self.update_values()

class RectTiny(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectTiny"
        self.Height = 22
        self.Width = 42
        Piece.__init__(self, x, y, r)
        self.update_values()
    

class RectSmall(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectSmall"
        self.Height = 22
        self.Width = 82
        Piece.__init__(self, x, y, r)
        self.update_values()


class RectMedium(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectMedium"
        self.Height = 22
        self.Width = 162
        Piece.__init__(self, x, y, r)
        self.update_values()


class RectBig(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectBig"
        self.Height = 22
        self.Width = 182
        Piece.__init__(self, x, y, r)
        self.update_values()


class RectFat(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "RectFat"
        self.Height = 42
        self.Width = 82
        Piece.__init__(self, x, y, r)
        self.update_values()


class SquareTiny(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "SquareTiny"
        self.Height = 22
        self.Width = 22
        Piece.__init__(self, x, y, r)
        self.update_values()


class SquareSmall(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "SquareSmall"
        self.Height = 42
        self.Width = 42
        Piece.__init__(self, x, y, r)
        self.update_values()


class Triangle(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "Triangle"
        self.Height = 72
        self.Width = 72
        Piece.__init__(self, x, y, r)
        self.update_values()


class TriangleHole(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "TriangleHole"
        self.Height = 82
        self.Width = 82
        Piece.__init__(self, x, y, r)
        self.update_values()


class SquareHole(Piece):
    def __init__(self, x=0, y=0, r=0):
        self.Name = "SquareHole"
        self.Height = 82
        self.Width = 82
        Piece.__init__(self, x, y, r)
        self.update_values()
        


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
    
    
clases = {
        '1':SquareHole, 
        '2':TriangleHole,
        }
clases["1"](22,22,80)