from collections import namedtuple

Author = namedtuple('Author', ['kdd_id', 'name', 'affiliation'])
RealAuthor = namedtuple('RealAuthor', ['kdd_author_ids', 'name', 'affiliation'])

