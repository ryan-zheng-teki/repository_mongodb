import logging
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from repository_mongodb.mongo_client import get_mongo_client
from functools import wraps  # Added import for wraps

logger = logging.getLogger(__name__)

@contextmanager
def transaction():
    client: MongoClient = get_mongo_client()
    session = client.start_session()
    try:
        session.start_transaction()
        logger.debug("Started MongoDB transaction")
        yield session
        session.commit_transaction()
        logger.debug("Committed MongoDB transaction")
    except PyMongoError as e:
        logger.exception("Exception occurred during MongoDB transaction, aborting", exc_info=e)
        session.abort_transaction()
        logger.debug("Aborted MongoDB transaction")
        raise
    finally:
        session.end_session()

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if a session is already provided
        if 'session' in kwargs and kwargs['session'] is not None:
            return func(*args, **kwargs)
        else:
            with transaction() as session:
                return func(*args, session=session, **kwargs)
    return wrapper