from contextlib import contextmanager
from callback import Callback


@contextmanager
def managed(sessionClass, auto_flush=False, callback=None):
    session = sessionClass()
    session.autoflush = auto_flush
    session.autocommit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        if isinstance(callback, Callback):
            callback()
        raise
    finally:
        session.close()


@contextmanager
def commit_on_success(session):
    try:
        yield session
        session.commit()
    except:
        raise
