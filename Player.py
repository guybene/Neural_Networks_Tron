import numpy as np
from math import inf as INFINITY, log2
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
MIN_AGENT = 1
MAX_AGENT = 0


class HumanPlayer:
    def __init__(self, index, color, path_color, pos, direction, keys):
        self.type = 'human'
        self.color = color
        self.path_color = path_color
        self.index = index
        self.pos = pos
        self.direction = direction
        self.left = keys[0]
        self.right = keys[1]
        self.up = keys[2]
        self.down = keys[3]

    def set_direction(self, key):
        if key not in [self.right, self.left, self.up, self.down]:
            return
        if key == self.left:
            self.direction = LEFT
        if key == self.right:
            self.direction = RIGHT
        if key == self.up:
            self.direction = UP
        if key == self.down:
            self.direction = DOWN


class NNPlayer:
    """
    agent using neural network in order to decide which action to take.
    """
    def __init__(self, index, color, path_color, pos, direction, neural_network=None):
        self.type = 'nn'
        self.color = color
        self.path_color = path_color
        self.index = index
        self.pos = pos
        self.direction = direction
        self.neural_network = neural_network

    def set_direction(self, input_vec):
        output = np.matmul(self.neural_network[0], input_vec) + self.neural_network[1]
        key = max(output)
        for i in range(len(output)):
            if key == output[i]:
                self.direction = i
                continue

    def set_nn(self, new_nn):
        self.neural_network = new_nn


class AlphaBetaPlayer:
    """
    agent using alpha beta algorithm to decide which action to take
    """
    def __init__(self, index, color, path_color, pos, direction, heuristic, depth=2):
        self.type = 'alpha_beta'
        self.index = index
        self.color = color
        self.path_color = path_color
        self.pos = pos
        self.direction = direction
        self.depth = depth
        self.heuristic = heuristic

    def evaluation_function(self, state):
        """
        Evaluation function, sum "dangers" from agent, the idea is to avoid danger areas.
        :param state: game state
        :return: sum of all dangers.
        """
        if not self.heuristic:
            return state.score
        counter = 0
        for i in range(1, self.pos[0] + 1):
            if not state.grid[self.pos[0] - i][self.pos[1]].clean:
                counter += i - 1
                break
        # scanning right
        for i in range(1, state.grid_size[0] - self.pos[0]):
            if not state.grid[self.pos[0] + i][self.pos[1]].clean:
                counter += i - 1
                break
        # scanning down
        for i in range(1, state.grid_size[1] - self.pos[1]):
            if not state.grid[self.pos[0]][self.pos[1] + i].clean:
                counter += i - 1
                break
        for i in range(1, self.pos[1] + 1):
            if not state.grid[self.pos[0]][self.pos[1] - i].clean:
                counter += i - 1
                break
        # scanning up left
        for i in range(1, min(self.pos[0], self.pos[1]) + 1):
            if not state.grid[self.pos[0] - i][self.pos[1] - i].clean:
                counter += i - 1
                break
        # scanning up right
        for i in range(1, min(state.grid_size[0] - 1 - self.pos[0], self.pos[1]) + 1):
            if not state.grid[self.pos[0] + i][self.pos[1] - i].clean:
                counter += i - 1
                break
        # scanning down right
        for i in range(1, min(state.grid_size[0] - 1 - self.pos[0], state.grid_size[1] - 1 - self.pos[1]) + 1):
            if not state.grid[self.pos[0] + i][self.pos[1] + i].clean:
                counter += i - 1
                break
        # scanning down left
        for i in range(1, min(self.pos[0], state.grid_size[1] - 1 - self.pos[1]) + 1):
            if not state.grid[self.pos[0] - i][self.pos[1] + i].clean:
                counter += i - 1
                break
        # normalizing vector according to "danger rate"
        return 1 / (1 + np.exp(-counter))

    def set_direction(self, game_state):
        """
        sets the agent direction according to alpha_beta pruning
        """
        legal_moves = game_state.get_legal_actions()
        successors = [game_state.generate_successor(0, action) for action in legal_moves]
        scores = [self.alpha_beta(1, MIN_AGENT, successor, -INFINITY, INFINITY) for successor in successors]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best
        self.direction = legal_moves[chosen_index]

    def alpha_beta(self, curr_depth, agent, state, alpha, beta):
        """
        alpha beta pruning algorithm, taken directly from ex3.
        """
        if curr_depth == 2 * self.depth or state.done:
            return state.score + self.evaluation_function(state)
        other_agent = 1 - agent
        successors = [state.generate_successor(agent, action) for action in state.get_legal_actions()]
        if agent == MAX_AGENT:
            for successor in successors:
                alpha = max(alpha, self.alpha_beta(curr_depth + 1, other_agent, successor, alpha, beta))
                if beta <= alpha:
                    break
            return alpha
        else:
            for successor in successors:
                beta = min(beta, self.alpha_beta(curr_depth + 1, other_agent, successor, alpha, beta))
                if beta <= alpha:
                    break
            return beta
