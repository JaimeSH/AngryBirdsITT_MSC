-------< Latest Patch notes below >-------- 

<<<<<<< HEAD
# Version 1.4 (5/08/2019 18:30)
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
=======
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
>>>>>>> 0796b9c74fb4c9d3f28c5c351999e67b1d9b79b8


# -------< General Information >-------- 
This project consisted in the generation of an evolutionary computation-based system capable of generate and evolve the structures of which one level of the Angry Birds game is composed, these structures are evaluated according to these particular rules:
•	The stability of the structure
•	The complexity of said structure

The current main values of the genetic algorithm are:

| Element  | Value |
| ------------- | ------------- |
| Population  | 10  |
| Max number of generations  | 5  |
| Pieces by individual *  | 10  |
| Selection type  |  Single-point, double-point and Uniform crossover  |
| Mutation percentage  | 40%  |
| Mutation type  | Random mutation, add value mutation, remove value mutation  |
| Selection type  | Ordered - top to bottom  |
