import logging
from contextlib import contextmanager
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from repository_mongodb.mongo_client import get_mongo_client, session_context_var
from functools import wraps

logger = logging.getLogger(__name__)

@contextmanager
def transaction():
    # First check if there's an existing session
    existing_session = session_context_var.get()
    if existing_session is not None:
        logger.debug("Reusing existing MongoDB session")
        try:
            # MongoDB doesn't support nested transactions, so we just yield the existing session
            yield existing_session
        except Exception as e:
            # Don't abort the transaction here as it's managed by the outer scope
            logger.debug("Exception in nested MongoDB transaction scope", exc_info=e)
            raise
        return

    # If no existing session, create a new one
    client: MongoClient = get_mongo_client()
    session = client.start_session()
    session_context_var.set(session)
    
    try:
        session.start_transaction()
        logger.debug("Started new MongoDB transaction")
        yield session
        
        if session.in_transaction:
            session.commit_transaction()
            logger.debug("Committed MongoDB transaction")
            
    except PyMongoError as e:
        logger.exception("Exception occurred during MongoDB transaction", exc_info=e)
        if session.in_transaction:
            session.abort_transaction()
            logger.debug("Aborted MongoDB transaction")
        raise
    except Exception as e:
        logger.exception("Unexpected error during MongoDB transaction", exc_info=e)
        if session.in_transaction:
            session.abort_transaction()
            logger.debug("Aborted MongoDB transaction due to unexpected error")
        raise
    finally:
        try:
            session.end_session()
            logger.debug("Ended MongoDB session")
        except Exception as e:
            logger.exception("Error while ending MongoDB session", exc_info=e)
        session_context_var.set(None)

def transactional(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction() as session:
            return func(*args, **kwargs)
    return wrapper