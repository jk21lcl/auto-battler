# support data augmentation

from random import random, randint
from math import floor

REPEAT_TIME = 2000  # the repetition times of each line of data
DISTURB_RATE = 0.2  # the disturb amplitude for each parameter
RANDOM_PROB = 0.3  
# the probability that using random choice, otherwise remain the 
# original choice

def clamp(value, min_value, max_value):
    return min(max_value, max(min_value, value))

def augment(input_path, output_path):
    fin = open(input_path, 'r')
    fout = open(output_path, 'w')
    min = [1, 0, 0, 1, 1, 0, 0, 1, 1]
    max = [100, 1000, 300, 10, 100, 1000, 300, 10, 25]
    
    for line in fin:
        fout.write(line)
        param = []
        for num in line.split():
            param.append(int(num))
        for _ in range(REPEAT_TIME):
            target = [floor(clamp(param[i] + (max[i] - min[i]) * (2 * random() - 1) * DISTURB_RATE, min[i], max[i])) for i in range(9)]
            choice = param[-1]
            if random() < RANDOM_PROB:
                choice = randint(0, 2)
            target.append(choice)
            for i in range(10):
                fout.write(str(target[i]) + " ")
            fout.write("\n")

if __name__ == "__main__":
    augment("data.txt", "augmented_data_2.txt")