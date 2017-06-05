from functools import wraps, partial

import numpy as np
from scipy.spatial import distance
from fuzzywuzzy import fuzz
import jellyfish


def distance_matrix(vector, distance_func):
    def metric(a, b):
        a = int(a[0])
        b = int(b[0])
        return distance_func(vector[a], vector[b])

    indices = np.arange(len(vector)).reshape(-1, 1)
    distance_vector = distance.pdist(indices, metric)
    distance_matrix = distance.squareform(distance_vector)
    return distance_matrix


def normalize_fuzzywuzzy_distance(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return 1 - result / 100
    return wrapper

ratio_distance = normalize_fuzzywuzzy_distance(fuzz.ratio)
partial_ratio_distance = normalize_fuzzywuzzy_distance(fuzz.partial_ratio)

token_sort_distance = normalize_fuzzywuzzy_distance(
    partial(fuzz._token_sort, partial=False, full_process=False)
)
partial_token_sort_distance = normalize_fuzzywuzzy_distance(
    partial(fuzz._token_sort, partial=True, full_process=False)
)
token_set_distance = normalize_fuzzywuzzy_distance(
    partial(fuzz._token_set, partial=False, full_process=False)
)
partial_token_set_distance = normalize_fuzzywuzzy_distance(
    partial(fuzz._token_set, partial=True, full_process=False)
)


def normalize_jellyfish_distance(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return 1 - result
    return wrapper

jaro_distance = normalize_jellyfish_distance(jellyfish.jaro_distance)
jaro_winkler_distance = normalize_jellyfish_distance(jellyfish.jaro_winkler)


def levenshtein(s1, s2):
    distance = jellyfish.levenshtein_distance(s1, s2)
    return distance / max(len(s1), len(s2))


def levenshtein_sort(s1, s2):
    s1_sorted = ' '.join(sorted(s1.split()))
    s2_sorted = ' '.join(sorted(s2.split()))
    return levenshtein(s1_sorted, s2_sorted)


def damerau_levenshtein(s1, s2):
    distance = jellyfish.damerau_levenshtein_distance(s1, s2)
    return distance / max(len(s1), len(s2))


def hamming(s1, s2):
    distance = jellyfish.hamming_distance(s1, s2)
    return distance / max(len(s1), len(s2))

