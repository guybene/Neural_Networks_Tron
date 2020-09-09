import random
import math
from operator import itemgetter
import numpy as np

class NN_MAT:
    NETWORKS_AMOUNT = 400
    SAMPLE_AMOUNT = 100
    INPUT_SIZE = 12
    OUTPUT_SIZE = 4

    def __init__(self):
        self.generation = 1
        self.networks1 = []
        self.networks2 = []
        for i in range(NN_MAT.NETWORKS_AMOUNT):
            weights1 = []
            for out in range(self.OUTPUT_SIZE):
                weights1.append([])
                for input in range(self.INPUT_SIZE):
                    weights1[out].append(np.random.uniform(-1,1))
            biases1 = []
            for bias in range(self.OUTPUT_SIZE):
                biases1.append(np.random.uniform(-1,1))
            self.networks1.append([[weights1,biases1],-math.inf])

            weights2 = []
            for out in range(self.OUTPUT_SIZE):
                weights2.append([])
                for input in range(self.INPUT_SIZE):
                    weights2[out].append(np.random.uniform(-1, 1))
            biases2 = []
            for bias in range(self.OUTPUT_SIZE):
                biases2.append(np.random.uniform(-1, 1))
            self.networks2.append([[weights2,biases2],-math.inf])
        self.networks = [self.networks1,self.networks2]

    def sort_networks(self):
        self.networks1 = sorted(self.networks1, key=itemgetter(1))
        self.networks[0] = self.networks1
        self.networks2 = sorted(self.networks2, key=itemgetter(1))
        self.networks[1] = self.networks2

    def create_next_gen(self):
        for player in range(2):
            network_index = 0
            for i in range(100):
                winn_weights = self.networks[player][self.NETWORKS_AMOUNT - 1 - i][0]
                for j in range(3):
                    curr_weights = self.networks[player][network_index][0]
                    mix_with = self.networks[player][random.randint(300,399)][0]
                    #Weights
                    for d1 in range(len(curr_weights[0])):
                        for d2 in range(len(curr_weights[0][d1])):
                            if np.random.binomial(1, 0.95,1) == 1:
                                curr_weights[0][d1][d2] = np.random.normal(winn_weights[0][d1][d2],2)
                            else:
                                curr_weights[0][d1][d2] = np.random.normal(mix_with[0][d1][d2],2)
                    #Bias
                    for d1 in range(len(curr_weights[1])):
                        if np.random.binomial(1, 0.95, 1) == 1:
                            curr_weights[1][d1] = np.random.normal(winn_weights[1][d1],2)
                        else:
                            curr_weights[1][d1] = np.random.normal(mix_with[1][d1],2)

                    self.networks[player][network_index][0] = curr_weights
                    network_index += 1
        self.generation += 1
        all_nets = self.networks1 + self.networks2
        random.shuffle(all_nets)
        self.networks1 = all_nets[:self.NETWORKS_AMOUNT]
        self.networks2 = all_nets[self.NETWORKS_AMOUNT:]
        self.networks = [self.networks1,self.networks2]
