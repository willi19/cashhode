import os
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
        num_tags = [len(tags) for tags in tags_list]
        plt.figure()
        plt.title(f'Dataset {filename}')
        plt.title('Tags per photo')
        plt.hist(num_tags, bins=100)
        plt.xlabel('# of tags')
        plt.ylabel('# of photos')
        plt.savefig(os.path.join('figures', filename.split('.')[0] + '.png'))
