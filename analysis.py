import os
from typing import List
import numpy as np
from matplotlib import pyplot as plt
from multiprocessing import Pool, cpu_count, Manager, Lock

from load import load
from ga import get_interest

FILENAMES = [
    'a.txt',
    'b.txt',
    'c.txt',
    'd.txt',
    'e.txt',
]

def get_nonzero_intersections(num_photos: int, tag_sets: List[set], index: int, lock: Lock, filename: str) -> int:
    nonzero = 0
    processes = cpu_count()
    for i in range(num_photos):
        for j in range(i + 1 + index, num_photos, processes):
            interest = get_interest(tag_sets[i], tag_sets[j])
            if interest > 0:
                nonzero += 1
                lock.acquire()
                try:
                    with open(os.path.join('outputs', filename.split('.')[0] + '.txt'), 'a') as file:
                        file.write(f'{i} {j}\n')
                finally:
                    lock.release()
    return nonzero

if __name__ == '__main__':
    os.makedirs('figures', exist_ok=True)
    os.makedirs('outputs', exist_ok=True)
    for filename in FILENAMES[:3]:
        num_photos, num_V, num_H, orients, num_tags, tags_list = load(filename)
        print(f'{filename}: {num_photos} photos, {num_V} vertical, {num_H} horizontal, {num_tags} total tags')
        num_tags = [len(tags) for tags in tags_list]
        # plt.figure(figsize=(12, 4))
        # plt.title(f'Dataset {filename}')
        # plt.subplot(1, 2, 1)
        # plt.title('Tags per photo')
        # plt.hist(num_tags, bins=100)
        # plt.xlabel('# of tags')
        # plt.ylabel('# of photos')

        # rng = np.random.default_rng()
        # interests = []
        nonzero = 0
        tag_sets = [set(tag_list) for tag_list in tags_list]

        with Pool(processes=cpu_count()) as pool:
            manager = Manager()
            lock = manager.Lock()
            processes = [pool.apply_async(get_nonzero_intersections, (num_photos, tag_sets, i, lock, filename)) for i in range(cpu_count())]
            # nonzeros = [process.get() for process in processes]
            # nonzero = sum(non[0] for non in nonzeros)
            # pairings = sum([non[1] for non in nonzeros], [])
            nonzero = sum(process.get() for process in processes)
        # with open(os.path.join('outputs', filename.split('.')[0] + '.txt'), 'w') as file:
        #     for pair in pairings:
        #         file.write(f'{pair[0]} {pair[1]}\n')
        print(f'Nonzero interest: {nonzero} out of {num_photos * (num_photos - 1) // 2}')
        # for _ in range(100000):
        #     indices = rng.choice(num_photos, size=2, replace=False)
        #     tag_set1 = set(tags_list[indices[0]])
        #     tag_set2 = set(tags_list[indices[1]])
        #     interest = min(len(tag_set1.difference(tag_set2)), len(tag_set2.difference(tag_set1)), len(tag_set1.intersection(tag_set2)))
        #     interests.append(interest)

        # print(f"Nonzero interest: {sum(i > 0 for i in interests)} out of 100,000")

        # plt.subplot(1, 2, 2)
        # plt.title('Randomly selected Interest factors')
        # plt.hist(interests, bins=100)
        # plt.xlabel('Interest factor')
        # plt.ylabel('# of pairs')
        # plt.savefig(os.path.join('figures', filename.split('.')[0] + '.png'))
        # plt.close()
