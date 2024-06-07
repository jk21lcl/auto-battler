import random
from search import Player
from scipy.spatial import KDTree

# if the distance exceeds the threshold, use random strategy
THRESHOLD = 0.5

def normalize(list):
    norm = [100, 1000, 300, 10, 100, 1000, 300, 10, 25]
    return [list[i] / norm[i] for i in range(9)]

def get_parameter(player : Player):
    return [player.health, player.attack, player.money, player.level]

def construct_kd_tree(data_path):
    dataset = []
    label = []
    with open(data_path, 'r') as file:
        for line in file:
            param = []
            for num in line.split():
                param.append(int(num))
            dataset.append(normalize(param[:-1]))
            label.append(param[-1])
    kdtree = KDTree(dataset)
    return kdtree, label

# choose an action based on dataset
# nearest is a flag indicating whether choosing the nearest neighbor
# do not modify the input
def dataset(self : Player, opponent : Player, round, kdtree : KDTree, label, nearest):
    choice = 0
    distance = 0
    param = get_parameter(self) + get_parameter(opponent) + [round]
    
    if nearest:
        distance, index = kdtree.query(normalize(param))
        choice = label[index]
    else:
        distances, indices = kdtree.query(normalize(param), k=2)
        distance = distances[1]
        choice = label[indices[1]]
    
    if distance > THRESHOLD:
        choice = random.randint(0, 2)
        
    return choice