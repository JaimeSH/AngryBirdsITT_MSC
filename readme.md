-------< Latest Patch notes below >-------- 

# Version 1.2.6 (2/21/2019 17:15)
    # Implemented
        - Added graphic with the results of the individuals on each generarion depending on the remaining of pieces and the movement of their original positions
        - Modified the xml generation code to prevent pieces to be placed on the same place creating a great dissaragement
        - Modified the evaluation methods to prevent errors when comparing the position of pieces that no longer exist after a simulation
        - Integration of the different masks based on the rule of thirds for placement of the composites
    
    # Pending
        - Integrate the use of different composites and pieces in the generation of individuals
        - Integrate mutation and different cross-over evaluations to the individuals
        - Implement a way to create and adapt the mask on different generations


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
