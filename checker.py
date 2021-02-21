from load import load as load
from time import time
from typing import List
import os
data_path = 'data'
filenames = ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt', 'f.txt']

def calc_interest_score(A: List[int], B: List[int]):
    p, q = set(A), set(B)
    return [ len(p - q), len(p & q), len(q - p) ]

def check(infname: str, oufname: str, submission: List[List[int]]):
    n, nv, nh, ori, nt, tags = load(infname)
    assert 1 <= len(submission) and len(submission) <= n
    shown_idx = set()
    sub_tag_list = []
    for L in submission:
        assert 1 <= len(L) and len(L) <= 2
        if len(L) == 1:
            x = L[0]
            assert 0 <= x and x < n
            assert x not in shown_idx
            assert ori[x] == 'H'
            sub_tag_list.append(tags[x])
        else:
            x, y = L[0], L[1]
            assert x != y
            assert 0 <= x and x < n
            assert 0 <= y and y < n
            assert ori[x] == 'V' and ori[y] == 'V'
            assert x not in shown_idx
            assert y not in shown_idx
            sub_tag_list.append(list( set(tags[x]) | set(tags[y]) ))

    bottleneck_count = [0] * 3
    score = 0
    print(sub_tag_list)
    for i, v in enumerate(sub_tag_list[:len(sub_tag_list) - 1]):
        w = sub_tag_list[i + 1]
        its = calc_interest_score(v, w)
        mi = min(list(range(3)), key=lambda i : its[i])
        print(its)
        score += its[mi]
        bottleneck_count[mi] += 1
    
    #dump phase
    print('score = ', score)
    print(f'Bottleneck occurrence: L-R: {bottleneck_count[0]}, L&R: {bottleneck_count[1]}, R-L: {bottleneck_count[2]}')
    dump(oufname, submission)

def get_name(fname):
    return fname + str(time()) + '.out'

def dump(fname:str, submission:List[List[int]]):
    fname = get_name(fname)
    path = os.path.join('output', fname)
    with open(path, 'w') as f:
        f.write(str(len(submission)) + '\n')
        for L in submission:
            f.write(' '.join([str(x) for x in L]) + '\n')

if __name__ == '__main__':
    check('a.txt', 'a_sample', [[0], [3], [1, 2]])
    check('a.txt', 'a_sample2', [[0], [1,2], [3]])
    check('a.txt', 'a_sample3', [[0, 3], [1, 2]])