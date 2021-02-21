import numpy as num
from load import load
from typing import List
import numpy as np
import random

from python_tsp.heuristics import solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming

L = 50

def calc_interest_score(A: List[int], B: List[int]):
    p, q = set(A), set(B)
    return min([ len(p - q), len(p & q), len(q - p) ])

FILENAMES = [
    'a.txt',
    'b.txt',
    'c.txt',
    'd.txt',
    'e.txt',
]

num_photos, num_V, num_H, orients, num_tags, tags_list = load(FILENAMES[1])


def get_dist_matrix(st, fin):
    dist = np.zeros((L+1,L+1))
    for i in range(L+1):
        for j in range(i+1,L+1):
            dist[i][j] = dist[j][i] = -calc_interest_score(tags_list[i+st],tags_list[j+st]) 
    return dist

def get_score(permute):
    ret = 0
    for i in range(num_photos-1):
        ret += calc_interest_score(tags_list[permute[i]],tags_list[permute[i+1]])
    return ret

def get_permutation(permute):
    ret = []
    st = 0
    for i in range(L+1):
        if permute[i] == L:
            st = i
            break        
    
    for i in range(st+1, L+1):
        ret.append(permute[i])
    
    for i in range(st):
        ret.append(permute[i])
    return ret
        
ans_max = [i for i in range(num_photos)]
print(get_score(ans_max))
it = 0
while True:
    if it%2 == 0:
        print(get_score(ans_max))
    st = random.randint(0,max(0,num_photos-L+1))
    fin = st+L-1
    dist = get_dist_matrix(st,fin)
    permutation, distance = solve_tsp_simulated_annealing(dist)
    permutation = get_permutation(permutation)
    new_ans = [ans_max[st+permutation[i]] for i in range(L)]
    for i in range(st,fin+1):
        ans_max[i] = new_ans[i-st]
    it+=1
    
    



