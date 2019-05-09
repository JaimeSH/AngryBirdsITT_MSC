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
        # Blocks must be a list like above
        self.blocks = blocks

    def height(self):
        #TO DO: Calculate height for blocks
        return 0.0

    def width(self):
        return 0.0

    def top_center(self):
        return 0.0

    def as_dictionary(self):
        return {}

    def as_json(self):
        return {}