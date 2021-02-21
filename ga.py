from load import load, FILENAMES

import numpy as np
from numpy.random import default_rng

def get_interest(tag_set1: set, tag_set2: set):
    return min(len(tag_set1.difference(tag_set2)), len(tag_set2.difference(tag_set1)), len(tag_set1.intersection(tag_set2)))

if __name__ == '__main__':
    rng = default_rng()
    num_population = 1e5
    for filename in FILENAMES:
        num_photos, num_V, num_H, orients, num_tags, tags_id_list = load(filename)
        for i in range(num_population):
            vertical_pairs = rng.shuffle(np.arange(num_V)).reshape(-1, 2)
            
