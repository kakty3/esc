import unicodedata
import re
from collections import OrderedDict
import functools

from esc_identifier.utils.common import compose
import nltk


def to_ascii(string):
    return (
        unicodedata.normalize('NFKD', string)
        .encode('ASCII', 'ignore')
        .decode('utf-8')
    )


def collapse_spaces(string):
    return re.sub("[ ]+", " ", string)


def remove_non_alpha_numeric_symbols(string):
    return re.sub("[^a-z0-9]", " ", string)


def remove_stopwords(string, stopwords):
    tokens = string.split(' ')
    token_no_stopwords = filter(lambda word: word not in stopwords, tokens)
    return ' '.join(token_no_stopwords)


def remove_duplicates(string):
    tokens = string.split(' ')
    unique_tokens = list(OrderedDict.fromkeys(tokens))
    return ' '.join(unique_tokens)


def normalize_string(string):
    return compose(
        collapse_spaces,
        remove_non_alpha_numeric_symbols,
        str.lower,
        to_ascii,
        str.strip
    )(string)


def normalize_human_name(string):
    return normalize_string(string)


affiliation_stopwords = {
    'university', 'department', 'college', 'school', 'lab', 'laboratory',
    'research', 'open', 'institute', 'academy'
}

# Spanish
affiliation_stopwords.update({
    'universidad', 'departamento', 'universidad', 'colegio',
    'laboratorio', 'investigacion', 'abierto', 'instituto', 'academia'
})

# Italian
affiliation_stopwords.update({
    'dipartimento', 'universita', 'scuola', 'laboratorio', 'ricerca',
    'aperto', 'istituto', 'accademia'
})

# French
affiliation_stopwords.update({
    'departement', 'universite', 'ecole', 'laboratoire', 'recherche',
    'ouvrir', 'institut', 'academie'
})

# Nederlands
affiliation_stopwords.update({
    'universiteit', 'afdeling', 'college', 'school', 'laboratorium',
    'onderzoek', 'open', 'instituut', 'academie'
})

affiliation_stopwords.update(
    nltk.corpus.stopwords.words()
)

remove_affiliation_stopwords =\
    functools.partial(remove_stopwords, stopwords=affiliation_stopwords)


def normalize_affiliation(string):
    string = compose(
        remove_duplicates,
        remove_affiliation_stopwords,
        normalize_string
    )(string)
    return string


