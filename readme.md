-------< Latest Patch notes below >-------- 

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