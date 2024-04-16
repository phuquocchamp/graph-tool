class Chromosome:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness

    def __str__(self):
        return str(self.genes) + " " + str(self.fitness)