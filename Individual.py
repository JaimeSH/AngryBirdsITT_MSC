class Individual:
    def __init__(self, **kwargs):
        #self.id = kwargs['id']
        #self.fitness = kwargs.get('fitness', {})
        self.chromosome = kwargs.get('chromosome', [])
        self.__dict__.update(kwargs)
        self.chromosome_objects = [Composites[composite] for composite in chromosome]

    def position_chromosome(self):
        #To do
        # Here you can use the chromosome objects etc.
        pass