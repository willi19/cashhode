import os
from typing import List, Tuple

def load(filename: str) -> Tuple[int, int, int, List[str], int, List[List[str]]]:
    file = open(os.path.join('data', filename))
    num_photos = int(file.readline())
    num_V = num_H = 0
    orients = []
    num_tags = []
    tags_list = []
    tag_set = set()
    for line in file.readlines():
        parse = line.split(' ')
        orient = parse[0]
        num_tag = int(parse[1])
        tags = parse[2:]

        if orient == 'V':
            num_V += 1
        elif orient == 'H':
            num_H += 1
        else:
            raise NotImplementedError

        orients.append(orient)
        num_tags.append(num_tag)
        tags_list.append(tags)
        tag_set.update(tags)

    return num_photos, num_V, num_H, orients, len(tag_set), tags_list
