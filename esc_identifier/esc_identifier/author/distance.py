
from esc_identifier.distance import token_set_distance
from esc_identifier.utils.string import (
    normalize_human_name, normalize_affiliation
)
from . import Author


distance_function = token_set_distance


def human_name_distance(a: str, b: str, normalize=False):
    return distance_function(
        normalize_human_name(a) if normalize else a,
        normalize_human_name(b) if normalize else b,
    )


# TODO: detect countries and cities
def affiliation_distance(a: str, b: str, normalize=False):
    return distance_function(
        normalize_affiliation(a) if normalize else a,
        normalize_affiliation(b) if normalize else b,
    )


def author_distance(a: Author, b: Author, normalize=False):
    distances_vector = [
        human_name_distance(a.name, b.name, normalize),
        affiliation_distance(a.affiliation, b.affiliation, normalize)
    ]
    return distances_vector
