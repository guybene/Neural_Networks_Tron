from NN_MAT import NN_MAT
from tron import*
from Player import*
import pickle


def training(iter_num):
    """
    start the iterative process of the genetic algorithm in order to find the best agent
    :param iter_num: number of generations
    :return:
    """
    nets = NN_MAT()
    p1 = NNPlayer(1, p1_color, p1_path_color, p1_pos, RIGHT)
    p2 = NNPlayer(1, p2_color, p2_path_color, p2_pos, LEFT)
    game = Tron(p1, p2)
    generations = []
    fitness = []
    total_fitness = 0
    for gen in range(iter_num):
        for i in range(len(nets.networks1)):
            p1.set_nn(nets.networks1[i][0])
            p2.set_nn(nets.networks2[i][0])
            if i < 395:
                score = game.run(False)[1]
            else:
                score = game.run(True)[1]
            nets.networks1[i][1] = score[0]
            nets.networks2[i][1] = score[1]
            total_fitness += game.counter
        print("Average fitness for generation",nets.generation, "is", total_fitness / 400)
        nets.sort_networks()
        fitness.append(total_fitness / 400)
        total_fitness = 0
        generations.append([nets.networks1[-1][0],total_fitness/400])
        nets.create_next_gen()


if __name__ == '__main__':
    print("Please choose one of the following options:")
    pick = input("1- Min-Max agent versus Neural-Network agent\n2- Min-Max agent versus human player"
                 "\n3- Neural-Network agent versus human player\n4- Watch the genetic algorithm progress,"
                 " each generation consists 400 games\nwe will run the first 395 games fast and then you can watch"
                 " the last 5 games for visualization purposes\n")
    while pick not in ['1', '2', '3', '4']:
        print("Invalid option, please choose one of the following options:")
        pick = input(
            "1- Min-Max agent versus Neural-Network agent\n2- Min-Max agent versus human player"
            "\n3- Neural-Network agent versus human player\n4- Watch the genetic algorithm progress,"
            " each generation consists 400 games\nwill run the first 395 games fast and then you can watch"
            " the last 5 games for visualization purposes\n")
    with open("GA_Results", 'rb') as f:
        list = pickle.load(f)
        neural_net = list[-1][0]
    if pick == '4':
        iter_num = input("Please select number of generations you wish to create (number between 1 - 300)\n")
        while iter_num not in [str(i) for i in range(1, 301)]:
            print("Invalid option, please choose one of the following options:")
            iter_num = input("Please select number of generations you wish to create (number between 1 - 300)\n")
        training(int(iter_num))
        exit()
    elif pick == '1':
        print("loading generation 300 Neural-Network agent")
        depth = input("choose depth of Min-Max agent (number between 1 - 4, 2 is recommended)\n")
        while depth not in ['1', '2', '3', '4']:
            print("Invalid option, please choose one of the following options:")
            depth = input("choose depth of Min-Max agent (number between 1 - 4, 2 is recommended)\n")
        heuristic = input("do you wish that the Min-Max agent will use heuristic ? (y / n)\n")
        while heuristic not in ['y', 'n']:
            print("Invalid option, please choose one of the following options:")
            heuristic = input("do you wish that the Min-Max agent will use heuristic ? (y / n)\n")
        p1 = AlphaBetaPlayer(MAX_AGENT, p1_color, p1_path_color, p1_pos, RIGHT, heuristic == 'y', int(depth))
        p2 = NNPlayer(1, p2_color, p2_path_color, p2_pos, LEFT, neural_net)
    elif pick == '2':
        depth = input("choose depth of Min-Max agent (number between 1 - 4, 2 is recommended)\n")
        while depth not in ['1', '2', '3', '4']:
            print("Invalid option, please choose one of the following options:")
            depth = input("choose depth of Min-Max agent (number between 1 - 4, 2 is recommended)\n")
        heuristic = input("do you wish that the Min-Max agent will use heuristic ? (y / n)\n")
        while heuristic not in ['y', 'n']:
            print("Invalid option, please choose one of the following options:")
            heuristic = input("do you wish that the Min-Max agent will use heuristic ? (y / n)\n")
        p1 = AlphaBetaPlayer(MAX_AGENT, p1_color, p1_path_color, p1_pos, RIGHT, heuristic == 'y', int(depth))
        p2_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        p2 = HumanPlayer(1, p2_color, p2_path_color, p2_pos, LEFT, p2_keys)
    else:
        p2_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        p2 = HumanPlayer(1, p2_color, p2_path_color, p2_pos, LEFT, p2_keys)
        p1 = NNPlayer(0, p1_color, p1_path_color, p1_pos, RIGHT, neural_net)
    game = Tron(p1, p2)
    game.run(False)
