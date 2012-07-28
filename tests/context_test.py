import unittest
import mock

from alchemytools.context import managed, commit_on_success


class BaseDumbSession(object):

    def commit(self):
        pass

    def close(self):
        pass

    def rollback():
        pass


class ManagedTest(unittest.TestCase):

    def setUp(self):
        self.mock_session = mock.Mock()

    def test_call_session_class(self):
        with managed(self.mock_session):
            assert self.mock_session.call_count == 1

    def test_set_autoflush_default_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = True

        with managed(MySession) as s:
            assert s.autoflush == False

    def test_set_autoflush_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = True

        with managed(MySession, auto_flush=True) as s:
            assert s.autoflush == True

    def test_set_autocommit_false(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autocommit = True

        with managed(MySession) as s:
            assert s.autocommit == False

    def test_commit_after_yield(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with managed(self.mock_session):
            pass
        assert 1 == real_session.commit.call_count

    def test_close_after_yield(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with managed(self.mock_session):
            pass
        assert 1 == real_session.close.call_count

    def test_rollback_on_exception(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        try:
            with managed(self.mock_session):
                raise Exception()
        except:
            pass
        assert 1 == real_session.rollback.call_count
        assert 0 == real_session.commit.call_count
        assert 1 == real_session.close.call_count

    def test_context_should_reraise_exceptions(self):
        raised = False
        try:
            with managed(mock.Mock()):
                raise Exception()
        except:
            raised = True
        assert raised


class CommitOnSuccessTest(unittest.TestCase):

    def test_commit_after_with_block(self):
        open_session = mock.Mock()
        with commit_on_success(open_session):
            pass
        assert 1 == open_session.commit.call_count

    def test_do_not_commit_if_exception_raised(self):
        open_session = mock.Mock()
        try:
            with commit_on_success(open_session):
                raise Exception()
        except:
            pass
        assert 0 == open_session.commit.call_count

    def test_context_should_reraise_exceptions(self):

        raised = False
        try:
            with commit_on_success(mock.Mock()):
                raise Exception()
        except:
            raised = True
        assert raised
