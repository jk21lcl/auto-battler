# multi-player 2-choice game
# the strategy is linear w.r.t health
# support figure plotting with different parameter

import random
import matplotlib.pyplot as plt
import numpy as np
import math

NUM_PLAYER = 2  # change the number of players

REPEAT_TIME = 1000  # test times for a strategy
PRECISION = 4  # the number of decimal digit
BASELINE = [0.5, 0.5]  # baseline
# Strategy is represented by a pair, where the first number is the upgrade 
# probability for health 100, and the second number is the upgrade 
# probability for health 0. The upgrade probability for other health
# is determined by linear interpolation.

INIT_HEALTH = 100  # initial health
UPGRADE_GAIN = 15  # the attack gain when upgrade
MONEY_PER_ROUND = 10  # the money players can get per round
MONEY_RATE = 0.1

def HealthLoss(round):  # the function of health loss if lose w.r.t. round
    return math.floor(5 + 0.5 * (round - 1))

def UpgradeCost(level):  # the function of cost of upgrade w.r.t. level
    return math.floor(0.25 * level * level * level - 2 * level * level + 7 * level)

def RefreshGain(level):  # the function of refresh gain w.r.t. level
    return 0.6 + 0.4 * (level - 1)

class Player:
    def __init__(self):
        self.health = INIT_HEALTH
        self.attack = 0
        self.level = 1
        self.money = 0
    
    def GetMoney(self):
        self.money += MONEY_PER_ROUND + math.floor(self.money * MONEY_RATE)
    
    def Update(self, strategy):  # 0 for upgrade, 1 for refresh
        if (strategy == 0):
            if (self.money >= UpgradeCost(self.level)):
                self.money -= UpgradeCost(self.level)
                self.attack += UPGRADE_GAIN
                self.level += 1
        else:
            self.attack += RefreshGain(self.level) * self.money
            self.money = 0
        self.attack = round(self.attack, PRECISION)
    
    def Battle(self, opponent_attack, round):
        if (opponent_attack > self.attack):
            self.health -= HealthLoss(round)
        elif (opponent_attack == self.attack):
            self.health -= HealthLoss(round) * 0.5

# prob_list[i] is a pair, representing the upgrade probability 
# w.r.t. health 100 and health 0
def checker(prob_list : list[list[int]]):
    player_list : list[Player] = []
    for _ in range(NUM_PLAYER):
        player_list.append(Player())
        
    def NumAlivePlayer():
        num_alive_player = 0
        for player in player_list:
            if player.health > 0:
                num_alive_player += 1
        return num_alive_player
    
    def GetMoney():
        for player in player_list:
            if player.health > 0:
                player.GetMoney()
    
    def Update():
        for i in range(NUM_PLAYER):
            if player_list[i].health > 0:
                actual_prob = prob_list[i][1] + (prob_list[i][0] - prob_list[i][1]) * player_list[i].health / 100
                player_list[i].Update(0 if random.random() < actual_prob else 1)
    
    def Battle(round):
        alive_list : list[int] = []
        for i in range(NUM_PLAYER):
            if (player_list[i].health > 0):
                alive_list.append(i)
        num_alive_player = len(alive_list)
        random.shuffle(alive_list)
        for i in range(num_alive_player // 2):
            player_list[alive_list[2 * i]].Battle(player_list[alive_list[2 * i + 1]].attack, round)
            player_list[alive_list[2 * i + 1]].Battle(player_list[alive_list[2 * i]].attack, round)
        if num_alive_player % 2 == 1:
            other_player = alive_list[:-1]
            player_list[alive_list[-1]].Battle(player_list[random.choice(other_player)].attack, round)
    
    round = 1
    alive = []
    while NumAlivePlayer() > 1:
        alive = [player_list[i].health > 0 for i in range(NUM_PLAYER)]
        GetMoney()
        Update()
        Battle(round)
        round += 1
    
    final_alive = [player_list[i].health > 0 for i in range(NUM_PLAYER)]
    
    if final_alive.count(1) == 1:
        return final_alive
    else:
        health_list = []
        for i in range(NUM_PLAYER):
            if alive[i]:
                health_list.append(player_list[i].health)
        max_health = max(health_list)
        scores = np.array([alive[i] and player_list[i].health == max_health for i in range(NUM_PLAYER)])
        return scores / np.sum(scores)

def compute_win_rate(upgrade_prob, baseline):
    test_prob_list = [upgrade_prob]
    for _ in range(NUM_PLAYER - 1):
        test_prob_list.append(baseline)
    scores = [0] * NUM_PLAYER
    for _ in range(REPEAT_TIME):
        result = checker(test_prob_list)
        for i in range(NUM_PLAYER):
            scores[i] += result[i]
    return scores[0] / REPEAT_TIME
    
if __name__ == "__main__":
    domain = np.linspace(0, 1, 100)
    win_rate = np.array([compute_win_rate([p, p], BASELINE) for p in domain])
    
    # used for figure plotting of different parameters
    
    # win_rate_list = []
    # for param in range(5):
    #     factor = param * 0.5
    #     win_rate_list.append(np.array([compute_win_rate([p, p * factor], BASELINE) for p in domain]))

    plt.figure()
    
    # for param in range(5):
    #     plt.plot(domain, win_rate_list[param], label=str(param * 0.5))
    
    plt.plot(domain, win_rate)
    
    plt.xlabel('prob of upgrade')
    plt.ylabel('win rate')
    plt.title('win rate of prob p v.s. [0.5, 0.5]')
    # plt.legend()
    plt.grid(True)
    plt.show()