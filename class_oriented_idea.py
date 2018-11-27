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


class Circle:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "Circle"
        self.__Height = 72
        self.__Width = 72
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list

class RectTiny:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "RectTiny"
        self.__Height = 22
        self.__Width = 42
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list
    

class RectSmall:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "RectSmall"
        self.__Height = 22
        self.__Width = 82
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class RectMedium:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "RectMedium"
        self.__Height = 22
        self.__Width = 162
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class RectBig:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "RectBig"
        self.__Height = 22
        self.__Width = 182
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class RectFat:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "RectFat"
        self.__Height = 42
        self.__Width = 82
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class SquareTiny:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "SquareTiny"
        self.__Height = 42
        self.__Width = 22
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class SquareSmall:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "SquareSmall"
        self.__Height = 42
        self.__Width = 22
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class Triangle:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "Triangle"
        self.__Height = 72
        self.__Width = 72
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class TriangleHole:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "TriangleHole"
        self.__Height = 82
        self.__Width = 82
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list


class SquareHole:
    def __init__(self, x=0, y=0, r=0):
        self.__Name = "SquareHole"
        self.__Height = 82
        self.__Width = 82
        self.__Material = "wood"
        self.X = x
        self.Y = y
        self.R = r
    
    def get_edges(self):
        ed_lis = []
        ed_lis.append([     self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self.__Heigth/2 +   self.Y,     self.__Width/2 + self.X])
        ed_lis.append([0 -  self..__Heigth/2 +  self.Y, 0 - self.__Width/2 + self.X])
        ed_lis.append([     self.__Heigth/2 +   self.Y, 0 - self.__Width/2 + self.X])
        self.__Edges = ed_list

    def get_points(self, r):
        ang = self.R * pi / 180
        ots = Rotate2D(self.__Edges, ar([0, 0]), ang)
        self.__Points = ost.tolist()

    def change_material(self, m):
        self.__Material = m

    def as_dictionary(self):
        self_list = []
        self_list.append(self.__Name)
        self_list.append(self.__Material)
        self_list.append(self.X)
        self_list.append(self.Y)
        self_list.append(self.R)
        self.__Dict = self_list