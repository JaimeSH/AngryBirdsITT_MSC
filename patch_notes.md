# Version 1.4.1 (5/09/2019 13:30)
    # Implemented
        - Modified the composites methods to obtain the top and bottom position for placement of pigs
        - Added a new method to create composites and add them to the pool of options at the beginning of the system
        - Added a "Mutation" method to calculate the positions for the pigs in a level
        - Modified the algorithm in order to restart the population once the fitness of it drops for various consecutive generations
        - Added the control of the configurations of the algorithm (not allowed pieces/combinations and pg quantity) according to a txt file
        - Changes to the fitness value calculation
            - Removed penalization by position and angle errors
            - Added criteria by calculating the shannon entroy on the composites of the chromosome
            - Added criteria by calculating the hamming distance on the best individual compared to all the other members of the population
        - Modifies the mask integration on the individuals to calculate the possible ending positions of the pigs on a level
        - Modified the XML generation code to integrate the pigs on the levels

    # Pending
        - Modify some individual class methods to preserve and modify the mask during generations and posibly combine it with another one
    
    # Extra
        - modified the final XY position for composites
        
# Version 1.3.2 (3/22/2019 13:40)
    # Implemented
        - Added mutation operation for the individual evolution
        - Modification to the selection algorithm
            - Removed random selection of parents
            - Added Roulette Style Selection
        - General modifications to the code
            - The calculation for the fitness is obtained at the begining of each geneation
            - A second calculation of fitness for the new individuals is obtained immediately after the integration to the population
        - Modification to the fitness calculation
    
    # Pending
        - Integrate the different cross-over evaluations to the individuals
        - Implement a way to create and adapt the mask on different generations
        - Clean the folders before beginning the algorithm

# Version 1.3.1 (3/07/2019 17:40)
    # Implemented
        - Integrated the use of different composites and pieces in the generation of individuals
        - Added support for linux distributions
    
    # Pending
        - Integrate mutation and different cross-over evaluations to the individuals
        - Implement a way to create and adapt the mask on different generations
        - Added integration with linux distributions but a bug prevents the generation to be calculated

# Version 1.3.0 (3/05/2019 18:20)
    # Implemented
        - Integrated the selection operations:
            - Random Selection
            - Tournament selection
        - Added a new instance of the AngryBirds app to use for the tournament selection
    
    # Pending
        - Integrate the use of different composites and pieces in the generation of individuals
        - Integrate mutation and different cross-over evaluations to the individuals
        - Implement a way to create and adapt the mask on different generations

# Version 1.2.9 (2/27/2019 18:27)
    # Implemented
        - Solved an error with the evaluation/generation code that caused an evaluation between a current gen individual with an individual form another generation
        - Modified the generation of the average fitness values of the individuals to reflect the error of movement and fitness by number of pieces
    
    # Pending
        - Integrate the use of different composites and pieces in the generation of individuals
        - Integrate mutation and different cross-over evaluations to the individuals
        - Implement a way to create and adapt the mask on different generations

# Version 1.2.8 (2/22/2019 14:01)
    # Implemented
        - Added graphic with the results of the individuals on each generarion depending on the remaining of pieces and the movement of their original positions
        - Modified the xml generation code to prevent pieces to be placed on the same place creating a great dissaragement
        - Modified the evaluation methods to prevent errors when comparing the position of pieces that no longer exist after a simulation
        - Integration of the different masks based on the rule of thirds for placement of the composites
    
    # Pending
        - Integrate the use of different composites and pieces in the generation of individuals
        - Integrate mutation and different cross-over evaluations to the individuals
        - Implement a way to create and adapt the mask on different generations

# Version 1.2.7 (2/20/2019 18:38)
    # Implemented
        - Modified existing code to acomodate the remaining pieces on the structure when the pieces exceeds a certain number

    # Pending
        - Analize the code to solve a problem where the remainig pieces added disarrange themselves
        - Integrate the use of different composites and pieces in the generation of individuals
        - Integrate mutation and different cross-over evaluations to the individuals

# Version 1.2.5 (2/20/2019 13:53)
    # Implemented
        - Implemented the mask adaptation for the individuals
        - Created a new class method to create a xml file if a individual is added to the elite pool
        - Changed the simulation code to execute it with a hidden window (A great time reduction)
        - Modified the create xml code to prevent pieces from going sky high

    # Pending
        - Randomize which mask will be used by each individual and add it to their data
        - Create a validation for the mask combination in case the number of pieces is not able to fill the areas
        - Integrate the use of different composites and pieces in the generation of individuals
        - Integrate mutation and different cross-over evaluations to the individuals