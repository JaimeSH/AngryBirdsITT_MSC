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
import hashlib


def fitness(ind_orig, ind_fin, chromosome, pop, pos):
    #print("Fitness = 100%")
    
    
    criteria = size_dif(ind_orig, ind_fin)
    criteria += (dif_pieces(chromosome) * 10) # 240
    criteria += calc_entropy(chromosome) * 100
    criteria += calc_hamming(chromosome, pop, pos)
    # total_fit = 100
    #size_pen = size_dif(ind_orig, ind_fin)
    #pos_pen = position_error(ind_orig, ind_fin)
    #total_fit = size_pen - pos_pen
    #size_fit = size_pen
    #pos_fit = pos_pen
    #print(size_pen)
    #print(pos_pen)
    #return [total_fit, size_fit, pos_fit]
    return [criteria, 100, 100]

def calc_hamming(chromosome, pop, pos):
    total = 0
    for c, chrom in enumerate(pop):
        if c != pos:
            total += hamming_distance(chromosome, chrom)
    return total


def calc_entropy(ind):
    # First calculate the frequency of the elements in array
    value_list = set(ind)

    freqList = []
    for piece in value_list:
        ctr = 0
        for ch in ind:
            if ch == piece:
                ctr += 1
        freqList.append(float(ctr) / len(ind))
    
    result = 0
    for e in freqList:
        result += (e*math.log(e,2))
    result = -result
    return result

def dif_pieces(b):
    #type_list = [piece[0] for piece in b]
    return len(set(b))

def size_dif(a, b):
    val_a = len(a)                      # Original amount
    val_b = len(b)                      # Remaining amount 
    percentage = (val_b * 100)/val_a    # Percentage to remove from total
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
        try:
            orig = a[int(piece[5])]
            error_xy = 0 if 1.0 > math.hypot((float(piece[2])) - (float(orig[2])), (float(piece[3])) - (float(orig[3]))) else ((100/len(a)) * 0.5)
            error_z = 0 if -5 < (abs(float(orig[4])) - abs(float(piece[4]))) < 5 else ((100/len(a)) * 0.5)
            total_error = total_error + error_xy + error_z
        except IndexError:
            #error_xy
            text = "Missing values - Pieces destroyed or something?..."
        #orig = a[int(piece[5])]
        #error_xy = 0 if 0.08 > math.hypot((float(piece[2])) - (float(orig[2])), (float(orig[3])) - (float(orig[3]))) else ((100/len(b)) * 0.5)
        #error_z = 0 if -5 < (abs(float(orig[4])) - abs(float(piece[4]))) < 5 else ((100/len(b)) * 0.5)
        #total_error = total_error + error_xy + error_z
    return total_error


def hamming_distance(a, b):
    # Calculate and return the Hamming distance of the two sets 
    return sum(c1 != c2 for c1, c2 in zip(a, b))