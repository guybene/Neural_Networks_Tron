from copy import*
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

MIN_AGENT = 1
MAX_AGENT = 0


def new_pos(player, action):
    if action == UP:
        new_x = player.pos[0]
        new_y = player.pos[1] -1
    elif action == DOWN:
        new_x = player.pos[0]
        new_y = player.pos[1] + 1
    elif action == RIGHT:
        new_x = player.pos[0] + 1
        new_y = player.pos[1]
    else:
        new_x = player.pos[0] - 1
        new_y = player.pos[1]
    return new_x, new_y


def update_grid(grid, player, pos):
    grid[player.pos[0]][player.pos[1]].change_color(player.path_color)
    player.pos = pos
    grid[player.pos[0]][player.pos[1]].change_color(player.color)


class State:
    """
    modeling our tron game as states.
    """
    def __init__(self, grid, max_player, min_player):
            self.grid = grid
            self.grid_size = [len(self.grid[0]), len(self.grid)]
            self.max_player = max_player
            self.min_player = min_player
            self.score = 0
            self.done = False

    def apply_action(self, action):
        """
        apply action to given state
        :param action: legal action
        :return: nothing.
        """
        new_x, new_y = new_pos(self.max_player, action)
        if new_x < 0 or new_x > self.grid_size[0] - 1 or new_y < 0 or new_y > self.grid_size[1] - 1:
            self.score = -1
            self.done = True
            return
        elif not self.grid[new_x][new_y].clean:
            self.score = -1
            self.done = True
            return
        update_grid(self.grid, self.max_player, (new_x, new_y))
        self.score = 0
        self.done = False

    def apply_opponent_action(self, action):
        new_x, new_y = new_pos(self.min_player, action)
        if new_x < 0 or new_x > self.grid_size[0] - 1 or new_y < 0 or new_y > self.grid_size[1] - 1:
            self.score = 1
            self.done = True
            return
        elif not self.grid[new_x][new_y].clean:
            self.score = 1
            self.done = True
            return
        update_grid(self.grid, self.min_player, (new_x, new_y))
        self.score = 0
        self.done = False

    def get_legal_actions(self):
        return [UP, DOWN, LEFT, RIGHT]

    def generate_successor(self, agent, action):
        """
        :param agent: agent type (min, max)
        :param action: legal action (U,D,L,R)
        :return: new state after applying this action.
        """
        new_grid = deepcopy(self.grid)
        new_max = deepcopy(self.max_player)
        new_min = deepcopy(self.min_player)
        new_state = State(new_grid, new_max, new_min)
        if agent == MIN_AGENT:
            new_state.apply_opponent_action(action)
        else:
            new_state.apply_action(action)
        return new_state
