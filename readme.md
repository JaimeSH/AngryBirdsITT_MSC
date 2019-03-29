-------< Latest Patch notes below >-------- 

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
