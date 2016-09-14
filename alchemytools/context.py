from alchemytools.callback import Callback


class managed(object):
    def __init__(self, sessionClass, auto_flush=False, auto_commit=False, callback=None, commit_on_success=True):
        self.session_class = sessionClass
        self.auto_flush = auto_flush
        self.auto_commit = auto_commit
        self.callback = callback
        self.commit_on_success = commit_on_success

    def _spawn_session(self):
        sess = self.session_class()
        sess.autoflush = self.auto_flush
        sess.autocommit = self.auto_commit
        self.session = sess
        return sess

    def _success(self):
        if self.commit_on_success:
            self.session.commit()

    def _fail(self, exc_val):
        self.session.rollback()
        if isinstance(self.callback, Callback):
            self.callback()

    def __enter__(self):
        return self._spawn_session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self._success()
        else:
            self._fail(exc_val)
        self.session.close()
        return False

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            try:
                f(self._spawn_session(), *args, **kwargs)
            except Exception as e:
                self._fail(e)
                raise e
            else:
                self._success()
            finally:
                self.session.close()
        return wrapped

