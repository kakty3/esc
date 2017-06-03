from collections import namedtuple

from esc_identifier.distance import token_set_distance
from esc_identifier.utils.string import (
    normalize_human_name, normalize_affiliation
)


Author = namedtuple('Author', ['kdd_id', 'name', 'affiliation'])
RealAuthor = namedtuple('RealAuthor', ['kdd_author_ids', 'name', 'affiliation'])


def human_name_distance(a: str, b: str, normalize=False):
    distance = token_set_distance
    return distance(
        normalize_human_name(a) if normalize else a,
        normalize_human_name(b) if normalize else b,
    )


# TODO: detect countries and cities
def affiliation_distance(a: str, b: str, normalize=False):
    distance = token_set_distance
    return distance(
        normalize_affiliation(a) if normalize else a,
        normalize_affiliation(b) if normalize else b,
    )


def author_distance(a: Author, b: Author, normalize=False):
    distances_vector = [
        human_name_distance(a.name, b.name, normalize),
        affiliation_distance(a.affiliation, b.affiliation, normalize)
    ]
    return distances_vector
