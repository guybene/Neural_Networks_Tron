import pygame
import random
from state import*
from Box import *
from Player import *
import pickle

#                                            SETTING CONSTANTS                                                       #
screen_size = (500, 500)
grid_size = [screen_size[0] // 20, screen_size[1] // 20]
grid_param = [screen_size[0] // grid_size[0], screen_size[1] // grid_size[1]]
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

TURN_LEFT = [1, 0, 0, 0]
TURN_RIGHT = [0, 1, 0, 0]
TURN_UP = [0, 0, 1, 0]
TURN_DOWN = [0, 0, 0, 1]


P1_SELF_DEATH = 1
P1_CRASHED_OTHER = -1
P2_SELF_DEATH = 2
P2_CRASHED_OTHER = -2
NON_TERMINAL = 3

#                                            COLOUR CONSTANTS                                                        #
p1_color = (255, 255, 255)
p2_color = (0, 255, 255)
p1_path_color = (255, 255, 0)
p2_path_color = (255, 0, 255)
p1_pos = [0, random.randint(0,grid_size[1]-1)]
p2_pos = [grid_size[0] - 1, random.randint(0,grid_size[1]-1)]
BLACK = (0, 0, 0)

#                                         HELPER METHODS                                                  #


def new_pos(player):
    if player.direction == UP:
        return player.pos[0], player.pos[1] - 1
    elif player.direction == DOWN:
        return player.pos[0], player.pos[1] + 1
    elif player.direction == RIGHT:
        return player.pos[0] + 1, player.pos[1]
    else:
        return player.pos[0] - 1, player.pos[1]


def create_boxes():
    boxes=[]
    for i in range(grid_size[0]):
        boxes.append([])
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            boxes[i].append(Box((i, j), grid_param))
    return boxes


def check_wall_collision(player):
    if player.pos[0] == 0 and player.direction == LEFT:
        return True
    elif player.pos[0] == grid_size[0] - 1 and player.direction == RIGHT:
        return True
    elif player.pos[1] == 0 and player.direction == UP:
        return True
    elif player.pos[1] == grid_size[1] - 1 and player.direction == DOWN:
        return True
    else:
        return False


def get_legal_moves(player):
    p_x = player.pos[0]
    p_y = player.pos[1]
    actions = [[p_x - 1, p_y], [p_x + 1, p_y], [p_x, p_y + 1], p_x, p_y - 1]


class Tron:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.input = []
        self.output = []
        self.p1 = player1
        self.p2 = player2
        self.p1_last_pos = player1.pos
        self.p2_last_pos = player2.pos
        self.grid = create_boxes()
        self.running = True
        self.counter = 0
        pygame.init()

    def game_rest(self):
        self.p1.pos = [0, random.randint(0,grid_size[1]-1)]
        self.p2.pos = [grid_size[0] - 1, random.randint(0,grid_size[1]-1)]
        self.p1_last_pos = self.p1.pos
        self.p2_last_pos = self.p2.pos
        self.grid = create_boxes()
        self.running = True
        self.counter = 0
        self.input = []
        self.output = []

    def generate_input(self, player):
        input_vec = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if player.index == self.p1.index:
            enemy = self.p2
        else:
            enemy = self.p1
        # scanning left
        input_vec[0] = player.pos[0]
        for i in range(1, player.pos[0] + 1):
            if not self.grid[player.pos[0] - i][player.pos[1]].clean:
                input_vec[0] = i - 1
                break
        # scanning right
        input_vec[1] = grid_size[0] - 1 - player.pos[0]
        for i in range(1, grid_size[0] - player.pos[0]):
            if not self.grid[player.pos[0] + i][player.pos[1]].clean:
                input_vec[1] = i - 1
                break
        # scanning down
        input_vec[2] = grid_size[1] - 1 - player.pos[1]
        for i in range(1, grid_size[1] - player.pos[1]):
            if not self.grid[player.pos[0]][player.pos[1] + i].clean:
                input_vec[2] = i - 1
                break
        # scanning up
        input_vec[3] = player.pos[1]
        for i in range(1, player.pos[1] + 1):
            if not self.grid[player.pos[0]][player.pos[1] - i].clean:
                input_vec[3] = i - 1
                break
        # scanning up left
        input_vec[4] = min(player.pos[0], player.pos[1])
        for i in range(1, min(player.pos[0], player.pos[1]) + 1):
            if not self.grid[player.pos[0] - i][player.pos[1] - i].clean:
                input_vec[4] = i - 1
                break
        # scanning up right
        input_vec[5] = min(grid_size[0] - 1 - player.pos[0], player.pos[1])
        for i in range(1, input_vec[5] + 1):
            if not self.grid[player.pos[0] + i][player.pos[1] - i].clean:
                input_vec[5] = i - 1
                break
        # scanning down right
        input_vec[6] = min(grid_size[0] - 1 - player.pos[0], grid_size[1] - 1 - player.pos[1])
        for i in range(1, input_vec[6] + 1):
            if not self.grid[player.pos[0] + i][player.pos[1] + i].clean:
                input_vec[6] = i - 1
                break
        # scanning down left
        input_vec[7] = min(player.pos[0], grid_size[1] - 1 - player.pos[1])
        for i in range(1, input_vec[6] + 1):
            if not self.grid[player.pos[0] - i][player.pos[1] + i].clean:
                input_vec[7] = i - 1
                break
        # normalizing vector according to "danger rate"
        for i in range(8):
            if input_vec[i] > 3:
                input_vec[i] = 0
            else:
                input_vec[i] = 3 - input_vec[i]
        # self coords:
        input_vec[8] = player.pos[0]
        input_vec[9] = player.pos[1]
        # enemy coords:
        input_vec[10] = enemy.pos[0]
        input_vec[11] = enemy.pos[1]
        return input_vec

    def paint_grid(self, screen):
        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                self.grid[i][j].draw_box(screen)

    def curr_move(self, player):
        if player.direction == LEFT:
            self.output.append(TURN_LEFT)
        elif player.direction == RIGHT:
            self.output.append(TURN_RIGHT)
        elif player.direction == UP:
            self.output.append(TURN_UP)
        else:
            self.output.append(TURN_DOWN)

    def check_state(self, pos):
        if pos[0] < 0 or pos[0] > grid_size[0] or pos[1] < 0 or pos[1] > grid_size[1]:
            return -1
        elif not self.grid[pos[0]][pos[1]].clean:
            return -1
        return 0

    def color_player(self):
        self.grid[self.p1_last_pos[0]][self.p1_last_pos[1]].change_color(self.p1.path_color)
        self.grid[self.p2_last_pos[0]][self.p2_last_pos[1]].change_color(self.p2.path_color)
        self.grid[self.p1.pos[0]][self.p1.pos[1]].change_color(self.p1.color)
        self.grid[self.p2.pos[0]][self.p2.pos[1]].change_color(self.p2.color)
        self.p1_last_pos = self.p1.pos
        self.p2_last_pos = self.p2.pos

    def check_path_collision(self, player):
        new = new_pos(player)
        return not self.grid[new[0]][new[1]].clean

    def update_position(self):
        new1 = new_pos(self.p1)
        new2 = new_pos(self.p2)
        self.p1.pos = new1
        self.p2.pos = new2

    def check_terminal(self):
        if check_wall_collision(self.p1):
            return P1_SELF_DEATH, [self.counter / 3, self.counter * 3]
        elif check_wall_collision(self.p2):
            return P2_SELF_DEATH, [self.counter * 3, self.counter / 3]
        elif self.check_path_collision(self.p1):
            new = new_pos(self.p1)
            if self.grid[new[0]][new[1]].color == self.p1.color:
                return P1_SELF_DEATH, [self.counter / 3, self.counter * 3]
            else:
                return P1_CRASHED_OTHER, [self.counter / 3, self.counter * 3]
        elif self.check_path_collision(self.p2):
            new = new_pos(self.p2)
            if self.grid[new[0]][new[1]].color == self.p2.color:
                return P2_SELF_DEATH, [self.counter * 3, self.counter / 3]
            else:
                return P2_CRASHED_OTHER, [self.counter * 3, self.counter / 3]
        return NON_TERMINAL


    def run(self, slow_mode):
        screen = pygame.display.set_mode(screen_size)
        self.game_rest()
        while self.running:
            self.counter += 1
            self.color_player()
            self.paint_grid(screen)
            pygame.display.update()
            if slow_mode:
                pygame.time.Clock().tick(10)
            for player in self.players:
                if player.type == 'nn':
                    player.set_direction(self.generate_input(player))
                elif player.type == 'alpha_beta':
                    curr_state = State(self.grid, self.p1, self.p2)
                    player.set_direction(curr_state)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    for player in self.players:
                        if player.type == 'human':
                            player.set_direction(event.key)
            state = self.check_terminal()
            if state is not NON_TERMINAL:
                return state
            self.update_position()


if __name__ == '__main__':
    input = "input_"
    output = "output_"

    for i in range(0, 10):
        with open("GA_Results", 'rb') as f:
            list = pickle.load(f)
            win_net1 = list[-15][0]
            win_net2 = list[-30][0]
        p1_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        p2_keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        # p1 = HumanPlayer(1, p1_color, p1_path_color, p1_pos, RIGHT, p1_keys)
        # p2 = HumanPlayer(1, p2_color, p2_path_color, p2_pos, LEFT, p2_keys)
        p1 = AlphaBetaPlayer(MAX_AGENT, p1_color, p1_path_color, p1_pos, RIGHT, True, 2)
        p2 = NNPlayer(1, p2_color, p2_path_color, p2_pos, LEFT, win_net2)
        game = Tron(p1, p2)
        game.run(True)
        # curr_in = input + str(i)
        # curr_out = output + str(i)
        # with open(curr_in, 'wb') as f:
        #     pickle.dump(game.input, f)
        # f.close()
        # with open(curr_out, 'wb') as f:
        #     pickle.dump(game.output, f)
        f.close()



