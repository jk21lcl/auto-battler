# 3-player 3-choice game

import math
import random
import numpy as np

PRECISION = 4  # the number of decimal digit

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
    def __init__(self, health = INIT_HEALTH, attack = 0, money = MONEY_PER_ROUND, level = 1):
        self.health = health
        self.attack = attack
        self.level = level
        self.money = money
    
    def GetMoney(self):
        self.money += MONEY_PER_ROUND + math.floor(self.money * MONEY_RATE)
    
    # 0 for upgrade, 1 for refresh, 2 for accumulate
    # 3 for dynamically upgrade to an appropriate level and then refresh
    def Update(self, strategy):
        if strategy == 0:
            while self.money >= UpgradeCost(self.level):
                self.money -= UpgradeCost(self.level)
                self.attack += UPGRADE_GAIN
                self.level += 1
        elif strategy == 1:
            self.attack += RefreshGain(self.level) * self.money
            self.attack = round(self.attack, PRECISION)
            self.money = 0
        elif strategy == 3:
            gain_list = []
            money = self.money
            level = self.level
            gain = 0
            gain_list.append(RefreshGain(level) * money)
            while money >= UpgradeCost(level):
                money -= UpgradeCost(level)
                gain += UPGRADE_GAIN
                level += 1
                gain_list.append(gain + RefreshGain(level) * money)
            index = gain_list.index(max(gain_list))
            
            for _ in range(index):
                self.money -= UpgradeCost(self.level)
                self.attack += UPGRADE_GAIN
                self.level += 1
            self.attack += RefreshGain(self.level) * self.money
            self.attack = round(self.attack, PRECISION)
            self.money = 0
    
    def Battle(self, opponent_attack, round):
        if (opponent_attack > self.attack):
            self.health -= HealthLoss(round)
        elif (opponent_attack == self.attack):
            self.health -= HealthLoss(round) * 0.5
    
    def ComputeUpgradeGain(self):
        money = self.money
        level = self.level
        gain = 0
        while money >= UpgradeCost(level):
            money -= UpgradeCost(level)
            gain += UPGRADE_GAIN
            level += 1
        return gain
    
    def ComputeRefreshGain(self):
        return RefreshGain(self.level) * self.money
    
    def Print(self):
        print(self.health, self.attack, self.money, self.level)

# compute the number of alive players
# do not modify the input
def NumAlivePlayer(player_list):
    num_alive_player = 0
    for player in player_list:
        if player.health > 0:
            num_alive_player += 1
    return num_alive_player

# compute the score of each player given the game is end
# alive is the list that represents whether player_i is alive in the 
# penultimate round
# do not modify the input
def ComputeScore(alive, final_health):
    final_alive = [final_health[i] > 0 for i in range(3)]
    if final_alive.count(1) == 1:
        return final_alive
    else:
        health_list = []
        for i in range(3):
            if alive[i]:
                health_list.append(final_health[i])
        max_health = max(health_list)
        cur_scores = np.array([alive[i] and final_health[i] == max_health for i in range(3)])
        cur_scores = cur_scores / np.sum(cur_scores)
        return cur_scores

# directly modify the input
def simulate_one_round(player_list : list[Player], cur_round, strategy):
    for i in range(3):
        if player_list[i].health > 0:
            player_list[i].Update(strategy[i])
    
    alive_list : list[int] = []
    for i in range(3):
        if (player_list[i].health > 0):
            alive_list.append(i)
    num_alive_player = len(alive_list)
    random.shuffle(alive_list)
    for i in range(num_alive_player // 2):
        player_list[alive_list[2 * i]].Battle(player_list[alive_list[2 * i + 1]].attack, cur_round)
        player_list[alive_list[2 * i + 1]].Battle(player_list[alive_list[2 * i]].attack, cur_round)
    if num_alive_player % 2 == 1:
        other_player = alive_list[:-1]
        if len(other_player):
            player_list[alive_list[-1]].Battle(player_list[random.choice(other_player)].attack, cur_round)
    
    cur_round += 1
    
    for player in player_list:
        if player.health > 0:
            player.GetMoney()
    
    return player_list, cur_round