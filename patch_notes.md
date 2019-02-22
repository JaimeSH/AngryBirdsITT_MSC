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