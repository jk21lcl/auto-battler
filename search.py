import random
import copy
from game_setting import Player, HealthLoss, NumAlivePlayer, ComputeScore, simulate_one_round

SEARCH_DEPTH = 3
REPEAT_TIME = 100  # simulation times

# use purely random strategy to simulate the game till end
# do not modify the input
def simulate(list : list[Player], cur_round):
    player_list = copy.deepcopy(list)
    round = cur_round
    alive = []
    
    while NumAlivePlayer(player_list) > 1:
        alive = [player_list[i].health > 0 for i in range(3)]
        strategy = [random.randint(0, 2) for _ in range(3)]
        player_list, round = simulate_one_round(player_list, round, strategy)
    
    return ComputeScore(alive, [player_list[i].health for i in range(3)])[0]

# use searching algorithm to choose an action
# assume the target player is the first player
# do not modify the input
def search(list : list[Player], cur_round):
    score_list = []
    
    # take the choice from right to left in base-3
    for i in range(3 ** SEARCH_DEPTH):
        score = 0
        for _ in range(REPEAT_TIME):
            player_list = copy.deepcopy(list)
            round = cur_round
            end = False
            
            for j in range(SEARCH_DEPTH):
                alive = [player_list[i].health > 0 for i in range(3)]
                choice_1 = (i // (3 ** j)) % 3
                choice_2 = 0 if player_list[1].ComputeUpgradeGain() > player_list[1].ComputeRefreshGain() else 1
                choice_3 = 2 if player_list[2].health > HealthLoss(round) else 3
                player_list, round = simulate_one_round(player_list, round, [choice_1, choice_2, choice_3])
                if NumAlivePlayer(player_list) <= 1:
                    score += ComputeScore(alive, [player_list[i].health for i in range(3)])[0]
                    end = True
                    break
            
            if not end:
                score += simulate(player_list, round)
            
        score_list.append(score)
    
    index = score_list.index(max(score_list))
    return index % 3