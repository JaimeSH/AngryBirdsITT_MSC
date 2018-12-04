# Evaluation metrics for the fitness of the individuals
#
# The metric to evaluate the fitness of an individual are:
# 1. If the number of pieces is different give a penalty
# 2. If the positioning of the pieces is diferent for more than 1 give a penalty
# The penalties are given has follows
# Initial fitness 100%
# - size_difference 
#       (remaining_pieces * 100) / original_pieces
# - position_error
#       for each piece
#           if the piece position is different by more than 2
#               ((1 * 100) / original_pieces)
#           else
#               ((1 * 100) / original_pieces) * (((abs(position) * 100) / 2) / 100)
# 
#            Check the angle
#               if different by more/less than ± 5 then penalize
#####################################################################################
#
# After the evaluation is over if a stable group remains in the file
# this group will be added to the pool of pieces
# 
#

from AngryBirdsGA import *
import math


def fitness(ind_orig, ind_fin):
    #print("Fitness = 100%")
    total_fit = 100
    size_pen = size_dif(ind_orig, ind_fin)
    pos_pen = position_error(ind_orig, ind_fin)
    total_fit = 100 - size_pen - pos_pen
    #print(size_pen)
    #print(pos_pen)
    return total_fit

def size_dif(a, b):
    val_a = len(a)                      # Original amount
    val_b = len(b)                      # Remaining amount 
    percentage = 100 - (val_b * 100)/val_a    # Percentage to remove from total
    return percentage

def position_error(a, b):
    total_error = 0
    for piece in b: 
        # 0 = Block     
        # 1 = Material    
        # 2 = x   
        # 3 = y   
        # 4 = r   
        # 5 = id
        orig = a[int(piece[5])]
        error_xy = 0 if 0.08 > math.hypot((float(piece[2])) - (float(orig[2])), (float(orig[3])) - (float(orig[3]))) else ((100/len(b)) * 0.5)
        error_z = 0 if -5 < (abs(float(orig[4])) - abs(float(piece[4]))) < 5 else ((100/len(b)) * 0.5)
        total_error = total_error + error_xy + error_z
    return total_error