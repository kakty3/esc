import logging
import logging.config
import itertools
import textwrap

import click
import time

from sqlalchemy.exc import StatementError
from python_utils.data_access import check_connection
from Bio import Medline
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from esc_identifier.database.models import Base, Author, Record

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')


@click.command()
@click.option('--db-uri', envvar='DB_URI')
@click.option('--drop-db', is_flag=True)
@click.argument('filename')
def parse(db_uri, filename, drop_db):
    check_connection(db_uri)

    sa_url = sa.engine.url.make_url(db_uri)
    sa_url.database = 'esc'

    engine = create_engine(sa_url)

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.bind = engine
    if drop_db:
        logger.info(f'Drop tables {list(Base.metadata.tables.keys())}')
        Base.metadata.drop_all()

    Base.metadata.create_all()

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    logger.info(f'Parsing file `{filename}`')

    with open(filename) as handle:
        tic = time.time()

        records = Medline.parse(handle)

        limit = 10000
        for record in itertools.islice(records, limit):
            record_authors = []
            try:
                full_authors_names = record['FAU']
            except KeyError:
                logging.error('Key `FAU` not found in record: '
                              f'{textwrap.shorten(str(record), width=50)}')
                continue

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

            session.add(new_record)
            try:
                session.commit()
            except StatementError as err:
                logger.error(err)
                session.rollback()

        toc = time.time()
        logger.debug(f'Parsed {limit} records in {toc - tic}s')


if __name__ == '__main__':
    parse()
