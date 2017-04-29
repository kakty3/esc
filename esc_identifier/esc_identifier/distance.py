import numpy as np
from scipy.spatial import distance
from fuzzywuzzy import fuzz


def distance_matrix(vector, distance_func):
    def metric(a, b):
        # a = int(a[0])
        # b = int(b[0])
        # return distance_func(vector[a], vector[b])
        return 0

    indices = np.arange(len(vector)).reshape(-1, 1)
    distance_vector = distance.pdist(indices, metric)
    distance_matrix = distance.squareform(distance_vector)
    return distance_matrix


def token_sort_distance(s1: str, s2: str):
    return 1 - fuzz.token_sort_ratio(s1, s2) / 100
