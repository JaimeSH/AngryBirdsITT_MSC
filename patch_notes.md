# Version 1.2.7 (2/20/2019 18:38)
    # Implemented
        - Modified existing code to acomodate the remaining pieces on the structure when the pieces exceeds a certain number

    # Pending
        Analize the code to solve a problem where the remainig pieces added disarrange themselves

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