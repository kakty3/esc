import logging
import unicodedata

import redis
import time

logger = logging.getLogger(__name__)


def redis_check_connection(url,
                           n_attempts: int = 10,
                           retry_interval: int = 2):
    r = redis.StrictRedis.from_url(url=url)

    for attempt in range(1, n_attempts + 1):
        try:
            r.ping()
        except redis.exceptions.ConnectionError:
            message = f'Attempt {attempt} of {n_attempts} failed'
            logger.debug(message)
            if attempt != n_attempts:
                time.sleep(retry_interval)
    else:
        message = f'Error connecting to redis on \'{url}\'.'
        raise ConnectionError(message)


def normalize_str(s):
    return (
        unicodedata.normalize('NFKD', s)
        .encode('ASCII', 'ignore')
        .decode('utf-8')
    )
