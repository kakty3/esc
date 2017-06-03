from collections import namedtuple

from esc_identifier.distance import token_set_distance
from esc_identifier.utils.string import (
    normalize_human_name, normalize_affiliation
)


Author = namedtuple('Author', ['kdd_id', 'name', 'affiliation'])
RealAuthor = namedtuple('RealAuthor', ['kdd_author_ids', 'name', 'affiliation'])


def human_name_distance(a: str, b: str):
    distance = token_set_distance
    a_normalized, b_normalized = \
        normalize_human_name(a), normalize_human_name(b)
    return distance(a_normalized, b_normalized)


# TODO: detect countries and cities
def affiliation_distance(a: str, b: str):
    distance = token_set_distance
    a_normalized, b_normalized = \
        normalize_affiliation(a), normalize_affiliation(b)
    return distance(a_normalized, b_normalized)


def author_distance(a: Author, b: Author):
    distances_vector = [
        human_name_distance(a.name, b.name),
        affiliation_distance(a.affiliation, b.affiliation)
    ]
    return distances_vector
