from typing import List
from copy import deepcopy

def pool_vertical_vertices(pic_h: List[int], pic_V: List[int], tags_list: List[List[int]], sample_stride = 10, num_exp = 5):
    solid_indices = deepcopy(pic_h)
    solid_tags = [tags_list[x].copy() for x in pic_h]
    

    