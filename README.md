# Auto Battler
Welcome to our code!

This is the code repository for 2024 game theory course project by group 1.

## Overview

- We implement multi-player auto battler game in our setting, and invent a method to compute win rate for strategies. We also support figure plotting of win rate for different parameters in game setting, such that game developers can reach a balanced game.
- We invent a search algorithm for 3-player game based on heuristic search. We also develop an augmented dataset of expert strategies and implement a strategy based on fictitious play as control group. Besides, we support an interface for human interaction with these strategies and performance testing among these strategies.

## Brief introduction of each file

- `multi_player.py` 

  Multi-player 2-choice game. Support figure plotting.

  - 2-choice: 0 for upgrading once, 1 for refreshing using all money.
  - Strategy is represented by a pair, where the first number is the upgrade probability for health 100, and the second number is the upgrade probability for health 0. The upgrade probability for other health is determined by linear interpolation.
  - Change the uppermost part of the code for adjustment of game setting.
  - Change the bottommost part of the code for the details of plotting figure. The code for plotting figures for different parameters is in the annotation.
  - Run the code to obtain the figure.

- `data.txt` 

  Raw data constructed by our group members.

  - The first 4 parameters are the health, attack, money, level for oneself, the following 4 parameters are the counterpart for the opponent, the last parameter is the current round.

- `augmented_data.txt` 

  Augmented data based on `data.txt`.

- `data_augmentation.py`

  Code for data augmentation.

  - Specify the input path and the output path, then directly run the code for generating augmented data.
