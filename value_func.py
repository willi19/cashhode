import os
import numpy as np
from matplotlib import pyplot as plt

from load import load

FILENAMES = [
    'a.txt',
    'b.txt',
    'c.txt',
    'd.txt',
    'e.txt',
]

if __name__ == '__main__':
    os.makedirs('figures', exist_ok=True)
    for filename in FILENAMES:
        num_photos, num_V, num_H, orients, num_tags, tags_list = load(filename)
        print(f'{filename}: {num_photos} photos, {num_V} vertical, {num_H} horizontal, {num_tags} total tags')
        if num_V == 0:
            continue
        tags_V_list = []
        for i in range(num_photos):
            if orients[i] == 'V':
                tags_V_list.append(tags_list[i])
                
        num_tags = [len(tags) for tags in tags_V_list]
        plt.figure(figsize=(12, 4))
        plt.title(f'Dataset {filename}')
        plt.subplot(1, 2, 1)
        plt.title('Tags per V_photo')
        plt.hist(num_tags, bins=100)
        plt.xlabel('# of tags')
        plt.ylabel('# of photos')

        rng = np.random.default_rng()
        interests = []
        for _ in range(100000):
            indices = rng.choice(num_V, size=2, replace=False)
            tag_set1 = set(tags_V_list[indices[0]])
            tag_set2 = set(tags_V_list[indices[1]])
            interest = len(tag_set1.intersection(tag_set2))
            interests.append(interest)

        print(f"Nonzero interest: {sum(i > 0 for i in interests)} out of 100,000")

        plt.subplot(1, 2, 2)
        plt.title('Randomly selected Interest factors')
        plt.hist(interests, bins=100)
        plt.xlabel('Interest factor')
        plt.ylabel('# of pairs')
        plt.savefig(os.path.join('figures_V', filename.split('.')[0] + '.png'))
        plt.close()
