from contextlib import contextmanager
from callback import Callback


@contextmanager
def managed(sessionClass, auto_flush=False, auto_commit=False, callback=None, commit_on_success=True):
    session = sessionClass()
    session.autoflush = auto_flush
    session.autocommit = auto_commit
    try:
        yield session
        if commit_on_success:
            session.commit()
    except:
        session.rollback()
        if isinstance(callback, Callback):
            callback()
        raise
    finally:
        session.close()

