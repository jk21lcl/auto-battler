import copy
import random

from game_setting import Player, NumAlivePlayer, simulate_one_round, ComputeScore
from search import search
from dataset import construct_kd_tree, dataset, KDTree
from fictitious import fictitious

REPEAT_TIME = 100
# the repeat times of the game
# set to 1 for human interaction
# set to large number (e.g. 100) for performance test

def select_mode():
    while True:
        s = input("Input the number of players (only support 2 or 3)\n")
        if s == '2' or s == '3':
            return int(s)
        print("Input out of range, please input again.")
        
def choose_type(index):
    while True:
        message = f"Select the type of player {index + 1}\n"
        message += "0 for human, 1 for search algorithm, 2 for dataset with nearest neighbor, "
        message += "3 for dataset with second nearest neighbor, 4 for fictitious play, "
        message += "5 for pure random strategy\n"
        s = input(message)
        if s == '0' or s == '1' or s == '2' or s == '3' or s == '4' or s == '5':
            return int(s)
        print("Input out of range, please input again.")

def show_status(player_list : list[Player], num_player):
    for i in range(num_player):
        player = player_list[i]
        print(f"player {i + 1}: health: {player.health} attack: {player.attack} money: {player.money} level: {player.level}")

def input_action(index):
    while True:
        s = input(f"Input action for player {index + 1}. 0 for upgrade, 1 for refresh, 2 for do nothing\n")
        if s == '0' or s == '1' or s == '2':
            return int(s)
        print("Input out of range, please input again.")

# do not modify the input
def choose_action(list : list[Player], round, i, type, num_player, kdtree : KDTree, label, history):
    if type == 0:
        return input_action(i)
    if type == 5:
        return random.randint(0, 2)
    if num_player == 2:
        j = (i + 1) % 2
        if type == 1:
            return search([list[i], list[j], copy.deepcopy(list[j])], round)
        if type == 2 or type == 3:
            nearest = (type == 2)
            return dataset(list[i], list[j], round, kdtree, label, nearest)
        if type == 4:
            return fictitious([list[i], list[j], copy.deepcopy(list[j])], round, history[j], history[j])
    if num_player == 3:
        j = (i + 1) % 3
        k = (i + 2) % 3
        if type == 1:
            return search([list[i], list[j], list[k]], round)
        if type == 2 or type == 3:
            nearest = (type == 2)
            opp = j if random.randint(0, 1) == 0 else k
            return dataset(list[i], list[opp], round, kdtree, label, nearest)
        if type == 4:
            return fictitious([list[i], list[j], list[k]], round, history[j], history[k])

if __name__ == "__main__":
    num_player = select_mode()
    types = [0] * num_player
    for i in range(num_player):
        types[i] = choose_type(i)
    human = True if 0 in types else False  # whether the game contains humans
    
    kdtree, label = construct_kd_tree("augmented_data.txt")
    
    scores = [0] * num_player
    for _ in range(REPEAT_TIME):
        player_list = [Player() for _ in range(3)]
        if num_player == 2:
            player_list[2] = Player(0)  # set the third player out
        
        round = 1
        history = [[0, 0, 0]] * num_player  # initialize the history
        
        while NumAlivePlayer(player_list) > 1:
            if human:
                print(f"Round: {round}")
                show_status(player_list, num_player)
            alive = [player_list[i].health > 0 for i in range(3)]
            actions = [0] * num_player
            for i in range(num_player):
                if player_list[i].health > 0:
                    actions[i] = choose_action(player_list, round, i, types[i], num_player, kdtree, label, history)
            if human:
                print(f"The action of each player is {actions}")
            if num_player == 2:
                actions.append(0)  # set 0 to be the strategy of player 3
            player_list, round = simulate_one_round(player_list, round, actions)
            for i in range(num_player):
                history[i][actions[i]] += 1  # update the history
        if human:
            show_status(player_list, num_player)
        score = ComputeScore(alive, [player_list[i].health > 0 for i in range(3)])
        for i in range(num_player):
            scores[i] += score[i]
    win_rate = [scores[i] / REPEAT_TIME for i in range(num_player)]
    print(f"Final scores: {scores}")
    print(f"Win rate: {win_rate}")