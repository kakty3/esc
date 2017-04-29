import logging
import textwrap

from Bio import Medline
from esc_identifier.database.models import Record, Author

logger = logging.getLogger(__name__)


def parse_record(record: Medline.Record) -> Record:
    try:
        full_authors_names = record['FAU']
    except KeyError:
        logging.error('Key `FAU` not found in record: '
                      f'{textwrap.shorten(str(record), width=50)}')
        return

    record_authors = []
    for full_author_name in full_authors_names:
        author_name_parts = full_author_name.split(', ')
        fore_name = author_name_parts[0]
        try:
              last_name = author_name_parts[1]
        except IndexError:
              last_name = None

        author = Author(
              fore_name=fore_name,
              last_name=last_name
        )
        record_authors.append(author)

    pmid = record['PMID']
    title = record['TI']
    try:
        abstract = record['AB'].strip()
    except KeyError:
        logging.warning('Key `AB` not found in record: '
                        f'{textwrap.shorten(str(record), width=50)}')
        abstract = ''

    new_record = Record(
        pmid=pmid,
        title=title,
        abstract=abstract,
        authors=record_authors
    )

    return new_record
