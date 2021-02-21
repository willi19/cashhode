from load import load, FILENAMES

if __name__ == '__main__':
    for filename in FILENAMES[:1]:
        num_photos, num_V, num_H, orients, num_tags, tags_id_list = load(filename)
