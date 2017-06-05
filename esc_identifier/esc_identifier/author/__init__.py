from collections import namedtuple

Author = namedtuple(
    'Author',
    [
        'kdd_id',
        'name',
        'affiliation',
        'coauthors'
    ]
)
RealAuthor = namedtuple('RealAuthor', ['kdd_author_ids', 'name', 'affiliation'])

