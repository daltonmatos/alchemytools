import unittest
import mock

from alchemytools.context import commit_on_success


class BaseDumbSession(object):

    def commit(self):
        pass

    def close(self):
        pass

    def rollback():
        pass


class CommitOnSuccessTest(unittest.TestCase):

    def setUp(self):
        self.mock_session = mock.Mock()

    def test_call_session_class(self):
        with commit_on_success(self.mock_session):
            assert self.mock_session.call_count == 1

    def test_set_autoflush_default_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = True

        with commit_on_success(MySession) as s:
            assert s.autoflush == False

    def test_set_autoflush_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = True

        with commit_on_success(MySession, auto_flush=True) as s:
            assert s.autoflush == True

    def test_set_autocommit_false(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autocommit = True

        with commit_on_success(MySession) as s:
            assert s.autocommit == False

    def test_commit_after_yield(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with commit_on_success(self.mock_session):
            pass
        assert 1 == real_session.commit.call_count

    def test_close_after_yield(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with commit_on_success(self.mock_session):
            pass
        assert 1 == real_session.close.call_count

    def test_rollback_on_exception(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        try:
            with commit_on_success(self.mock_session):
                raise Exception()
        except:
            pass
        assert 1 == real_session.rollback.call_count
        assert 0 == real_session.commit.call_count
        assert 1 == real_session.close.call_count
