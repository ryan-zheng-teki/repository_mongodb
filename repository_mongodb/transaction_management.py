import logging
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from repository_mongodb.mongo_client import get_mongo_client, session_context_var
from functools import wraps

logger = logging.getLogger(__name__)

@contextmanager
def transaction():
    client: MongoClient = get_mongo_client()
    session = client.start_session()
    
    # Check if there's already an active session
    existing_session = session_context_var.get()
    if existing_session is not None:
        # Use existing session for nested transaction
        yield existing_session
        return

    # Set the session in context
    token = session_context_var.set(session)
    
    try:
        session.start_transaction()
        logger.debug("Started MongoDB transaction")
        yield session
    except PyMongoError as e:
        logger.exception("Exception occurred during MongoDB transaction", exc_info=e)
        if session.in_transaction:
            session.abort_transaction()
            logger.debug("Aborted MongoDB transaction")
        raise
    finally:
        if session.in_transaction:
            # Only try to commit if we haven't aborted
            try:
                session.commit_transaction()
                logger.debug("Committed MongoDB transaction")
            except PyMongoError as e:
                logger.exception("Error committing transaction", exc_info=e)
                session.abort_transaction()
                logger.debug("Aborted MongoDB transaction due to commit error")
                raise
        session_context_var.reset(token)

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction() as session:
            return func(*args, **kwargs)
    return wrapper