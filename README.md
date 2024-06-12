# Auto Battler
Welcome to our code!

This is the code repository for 2024 game theory course project by group 1.

## Overview

- We implement multi-player auto battler game in our setting, and invent a method to compute win rate for strategies. We also support figure plotting of win rate for different parameters in game setting, such that game developers can reach a balanced game.
- We invent a search algorithm for 3-player game based on heuristic search. We also develop an augmented dataset of expert strategies and implement a strategy based on fictitious play as contrast group. Besides, we support an interface for human interaction with these strategies and performance testing among these strategies.

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

- `game_setting.py`

  3-player 3-choice game.

  - 3-choice: 0 for upgrading as much as possible, 1 for refreshing using all money, 2 for doing nothing.

- `search.py`

  Code for search algorithm.

- `dataset.py`

  Code for choosing actions based on dataset.

- `fictitious.py`

  Code for choosing actions using fictitious play.

- `interface.py`

  Interact with the strategies and conduct performance test.

  - First enter the number of players (only support 2 or 3 players), then enter the type for each player. There are 6 types of players: human, search algorithm, dataset with nearest neighbor, dataset with second nearest neighbor, fictitious play, pure random.

    Run the code to get the final scores of each player.

  - For human interaction, set `REPEAT_TIME` to be 1; for performance test, set `REPEAT_TIME` to be a large number (e.g. 100).
  
  - It will save the win rate to `output.txt` for every 100 iterations.

- `dataset_vs_random.txt`

  The output file for dataset with nearest neighbor v.s. (random strategies $\times$​​ 2).

  - The average win rate of dataset is 58.1% (note that 3 identical players will have 33.3% win rate on average), which implies that the expert strategies are indeed better than pure random strategies.

- `search_vs_dataset.txt`

  The output file for search algorithm v.s. (dataset with nearest neighbor + dataset with second nearest neighbor).

  - The average win rate of search algorithm is 89.3%, which implies that our search algorithm is even better than the expert strategies.

- `search_vs_fictitious.txt`

  The output file for search algorithm v.s. (fictitious play $\times$​ 2).
  
  - The average win rate of search algorithm is 100.0%, which means that our search algorithm can completely defeat fictitious play.
