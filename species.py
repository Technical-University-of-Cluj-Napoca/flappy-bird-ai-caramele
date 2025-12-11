import operator
import random

class Species:
    def __init__(self, player):
        self.players = []
        self.average_fitness = 0
        self.threshold = 1.2
        self.players.append(player)
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone()
        self.champion = player.clone()

    def similarity(self, brain):
        similarity = self.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity

    @staticmethod
    def weight_difference(brain1, brain2):
        total_weight_diff = 0
        for i in range(0, len(brain1.connections)):
            for j in range(0, len(brain2.connections)):
                if i==j:
                    total_weight_diff += abs(brain1.connections[i].weight
                                             - brain2.connections[j].weight)
        return total_weight_diff

    def add_to_species(self, player):
        self.players.append(player)

    def sort_players_by_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)
        if self.players[0].fitness > self.benchmark_fitness:
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()

    def calculate_average_fitness(self):
        total_fitness = 0
        for p in self.players:
            total_fitness += p.fitness
        if self.players:
            self.average_fitness = int(total_fitness) / len(self.players)
        else:
            self.average_fitness = 0

    def offspring(self):
        baby = self.players[random.randint(1,len(self.players))-1].clone()
        baby.brain.mutate()
        return baby

