from contextlib import contextmanager
from callback import Callback


class managed(object):
    def __init__(self, sessionClass, auto_flush=False, auto_commit=False, callback=None, commit_on_success=True):
        self.session_class = sessionClass
        self.auto_flush = auto_flush
        self.auto_commit = auto_commit
        self.callback = callback
        self.commit_on_success = commit_on_success

    def __enter__(self):
        sess = self.session_class()
        sess.autoflush = self.auto_flush
        sess.autocommit = self.auto_commit
        self.session = sess
        return sess

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.commit_on_success:
                self.session.commit()
        else:
            self.session.rollback()
            if isinstance(self.callback, Callback):
                self.callback()
        self.session.close()
        return False

