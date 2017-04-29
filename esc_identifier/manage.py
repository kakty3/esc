import logging.config
import itertools
import time

import click
import redis
import json
from sqlalchemy.exc import StatementError
from python_utils.data_access import check_connection as pg_check_connection
from Bio import Medline
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from esc_identifier.database.models import Base, Author
from esc_identifier.training_data_generator import (
    get_trainconfirmed_authors_ids,
    get_author_name_variations,
    get_affiliation_variants
)
from esc_identifier.parse import parse_record
from esc_identifier.distance import (distance_matrix,
                                     token_sort_distance)
from esc_identifier.cluster import dbscan, load_clusters
from esc_identifier.utils import normalize_str

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')


@click.group()
def manager():
    pass


@manager.command('import')
@click.option('--db-uri', envvar='DB_URI')
@click.option('--drop-db', is_flag=True)
@click.argument('filename')
def import_(db_uri, filename, drop_db):
    check_connection(db_uri)

    sa_url = sa.engine.url.make_url(db_uri)

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

    logger.info(f'Importing records from \'{filename}\'')

    with open(filename) as handle:
        tic = time.time()

        records = Medline.parse(handle)

        limit = 10000
        for record in itertools.islice(records, limit):
            new_record = parse_record(record)

            session.add(new_record)
            try:
                session.commit()
            except StatementError as err:
                logger.error(err)
                session.rollback()

        toc = time.time()
        logger.debug(f'Parsed {limit} records in {toc - tic}s')


@manager.command()
@click.option('--db-uri', envvar='DB_URI')
@click.option('--limit', envvar='ESC_LIMIT', default=1000)
def cluster_authors(db_uri, limit):
    check_connection(db_uri)

    sa_url = sa.engine.url.make_url(db_uri)

    engine = create_engine(sa_url)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    logger.debug(f'Limit={limit}')

    authors = session.query(Author).limit(limit).all()

    logger.debug('Calculating distance matrix')
    # TODO: make contextwrapper for timer
    tic = time.time()
    # TODO: add lowercase'ing to distance function
    authors_distance_matrix = distance_matrix(
        [author.to_str() for author in authors],
        token_sort_distance
    )
    logger.info(f'Distance matrix calculated in {time.time() - tic} s')

    items_indices = list(range(len(authors)))

    tic = time.time()
    clusters = dbscan(items_indices, authors_distance_matrix, eps=0.1)

    logger.info(f'DBSCAN for {len(authors)} items done in {time.time() - tic} s')
    logger.info(f'Found {len(clusters)} clusters')

    clusters_filename = '/opt/data/clusters.json'
    with open(clusters_filename, 'w') as outfile:
        json.dump(
            [
                [authors[i].to_str() for i in cluster]
                for cluster
                in clusters
            ],
            outfile,
            indent=2
        )

    logger.info(f'Saved clusters to `{clusters_filename}`')


@manager.command()
@click.option('--min-size', default=1, type=int)
def show_authors_clusters(min_size):
    authors_clusters = load_clusters('/opt/data/clusters.json')

    for cluster in authors_clusters:
        if len(cluster) >= min_size:
            logger.debug(cluster)


@manager.command()
@click.option('--kdd-db-uri', envvar='KDD_DB_URI')
def show_kdd_authors(kdd_db_uri):
    pg_check_connection(kdd_db_uri)

    sa_url = sa.engine.url.make_url(kdd_db_uri)

    engine = create_engine(sa_url)
    Base.metadata.bind = engine
    Base.metadata.reflect()

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    author_name_and_affiliation_variations = {}

    authors_ids = get_trainconfirmed_authors_ids(session)
    logger.debug(
        f'Fetched ids for {len(authors_ids)} authors'
        'from "trainconfirmed" table'
    )

    authors_ids_number_width = len(str(len(authors_ids)))

    # logger.debug('Fetching name and affiliation variations')
    for i, author_id in enumerate(authors_ids, 1):
        # logger.debug(f'authorid={author_id}')
        name_variations = get_author_name_variations(session, author_id)
        normalized_name_variations = [
            normalize_str(name)
            for name
            in name_variations
        ]
        # logger.debug(f'name variations: {name_variations}')

        affiliation_variations = get_affiliation_variants(session, author_id)
        normalized_affiliation_variations = [
            normalize_str(affiliation)
            for affiliation
            in affiliation_variations
        ]
        # logger.debug(f'affiliation variations: {affiliation_variations}')

        author_name_and_affiliation_variations[author_id] = {
            'names': normalized_name_variations,
            'affiliations': normalized_affiliation_variations,
        }
        # logger.debug(f'Fetched data for {i} of {len(authors_ids)} authors')
        logger.debug(
            'Fetching name and affiliation variations: '
            f'{i:{authors_ids_number_width}}/{len(authors_ids)}'
        )

    out_file_path = '/opt/data/author_name_and_affiliation_variations.json'

    with open(out_file_path, 'w') as out_file:
        json.dump(author_name_and_affiliation_variations, out_file, indent=2)

    logger.info(f'Data saved to {out_file_path}')


if __name__ == '__main__':
    manager()
