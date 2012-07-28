from contextlib import contextmanager


@contextmanager
def managed(sessionClass, auto_flush=False):
    session = sessionClass()
    session.autoflush = auto_flush
    session.autocommit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
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
