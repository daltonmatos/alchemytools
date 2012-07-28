from contextlib import contextmanager


@contextmanager
def commit_on_success(sessionClass, auto_flush=False):
    session = sessionClass()
    session.autoflush = auto_flush
    yield session
