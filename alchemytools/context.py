from contextlib import contextmanager


@contextmanager
def commit_on_success(sessionClass):
    yield sessionClass()
