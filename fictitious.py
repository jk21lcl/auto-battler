import copy
from game_setting import Player, simulate_one_round, HealthLoss

# choose an action using fictitious play
# h_i is the counter for historical choices of player_i
# assume the target player is the first player
# do not modify the input
def fictitious(list : list[Player], cur_round, h_2, h_3):
    scores = [0, 0, 0]
    for s_1 in range(3):
        for s_2 in range(3):
            for s_3 in range(3):
                player_list = copy.deepcopy(list)
                round = cur_round
                player_list, round = simulate_one_round(player_list, round, [s_1, s_2, s_3])
                lost_health = list[0].health - player_list[0].health
                score = 0
                if lost_health == 0:
                    score = 1
                elif lost_health == 0.5 * HealthLoss(cur_round):
                    score = 0.5
                scores[s_1] += score * h_2[s_2] * h_3[s_3]
    # choose the strategy with max score, use larger index to break tie
    scores.reverse()
    return 2 - scores.index(max(scores))