import logging
from functools import wraps

logger = logging.getLogger(__name__)


class DbTransactionManager:
    def __init__(self,session):
        self.session = session

    def __enter__(self):
        pass

    def __exit__(self,e,etype,traceback):
        if not e:
            # No exceptions let's commit
            # logger.info("transaction ok, but not committing, because of sqlalchemy funnyness.")
            if self.session:
                logger.debug("DBTM: COMMIT")
                self.session.commit()
        else:
            # an exception happened let's rollback
            if self.session:
                logger.info("DBTM: ROLLBACK!")
                self.session.rollback()
            return False


def managedtrans():
    from liveapi.extensions import db

    def decorator(function):
        @wraps(function)
        def inner(*args,**kwargs):
            with DbTransactionManager(db.session) as dtm:
                return function(*args,**kwargs)

        return inner

    return decorator
