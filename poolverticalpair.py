from typing import List, Set
from copy import deepcopy
from random import shuffle, randint
from checker import dump

def calc_interest_score(p, q):
    return min([ len(p - q), len(p & q), len(q - p) ])

def randomly_match(remaining_indices):
    shuffle(remaining_indices)
    return [[remaining_indices[i], remaining_indices[i+1]] for i in range(0, len(remaining_indices), 2)]

def pool_vertical_vertices(pic_h: List[int], pic_v: List[int], tags_list: List[List[int]], sample_stride = 10, num_exp = 50, hear_horizontal = False):
    solid_indices = [[x] for x in pic_h]
    solid_tags = [set(tags_list[x]) for x in pic_h]
    
    remaining_indices = pic_v.copy()
    while len(remaining_indices) > 1:
        pairs = randomly_match(remaining_indices)
        tagsets = [set(tags_list[p[0]]) | set(tags_list[p[1]]) for p in pairs]
        P = len(pairs)
        if P == 1:
            solid_indices.append(pairs[0])
            solid_tags.append(tagsets[0])
            break
        scores = [0] * P
        exp_counts = [0] * P
        for i in range(P):
            for _ in range(num_exp):
                action_type = randint(0, 1)
                if not hear_horizontal and len(solid_indices) == len(pic_h):
                    action_type = 1 #resolve the case when there's no solid verticals
                if action_type <= 0: #interaction with solid ones
                    j = -1
                    if hear_horizontal:
                        j = randint(0, len(solid_indices) - 1)
                    else:
                        j = randint(len(pic_h), len(solid_indices) - 1)
                    exp_counts[i] += 1
                    scores[i] += calc_interest_score(tagsets[i], solid_tags[j])
                else:
                    j = i
                    while j == i:
                        j = randint(0, P-1)
                    new_score = calc_interest_score(tagsets[i], tagsets[j])
                    exp_counts[i] += 1
                    scores[i] += new_score
                    exp_counts[j] += 1
                    scores[j] += new_score
        for i in range(P):
            scores[i] /= exp_counts[i]
        index_selector = list(range(P))
        index_selector.sort(key=lambda i : -scores[i])
        selected = index_selector[:sample_stride]
        non_selected = index_selector[sample_stride:]
        for s in selected:
            solid_indices.append(pairs[s])
            solid_tags.append(tagsets[s])
        tmp = []
        for ns in non_selected:
            tmp += pairs[ns]
        remaining_indices = tmp
    return solid_indices, solid_tags

if __name__ == '__main__':
    from load import load
    n, nv, nh, ori, nt, tags = load('c.txt')
    h = list(filter(lambda x : ori[x] == 'H', range(n)))
    v = list(filter(lambda x : ori[x] == 'V', range(n)))
    #print(h, v)
    print(nh, nv)
    solid_indices, _ = pool_vertical_vertices(h, v ,tags, sample_stride = 20, num_exp = 200)
    dump('c_test', solid_indices)
    