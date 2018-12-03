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
#           if the piece is positiones different by more than 2
#               ((1 * 100) / original_pieces)
#           else
#               ((1 * 100) / original_pieces) * (((abs(position) * 100) / 2) / 100)
# 
#####################################################################################
#
# After the evaluation is over if a stable group remains in the file
# this group will be added to the pool of pieces
# 
#

from AngryBirdsGA import *


def fitness(ind_orig, ind_fin):
    #print("Fitness")

    print(ind_fin)
    return 0

def size_dif(a, b):

    return 0

def position_error(a, b):

    return 0