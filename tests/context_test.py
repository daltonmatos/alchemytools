import unittest
import mock

from alchemytools.context import commit_on_success


class CommitOnSuccessTest(unittest.TestCase):

    def setUp(self):
        self.mock_session = mock.Mock()

    def test_call_session_class(self):
        with commit_on_success(self.mock_session):
            assert self.mock_session.call_count == 1

    def test_set_autoflush_default_value(self):
        class MySession(object):
            def __init__(self):
                self.autoflush = True
        with commit_on_success(MySession) as s:
            assert s.autoflush == False

    def test_set_autoflush_value(self):
        class MySession(object):
            def __init__(self):
                self.autoflush = True
        with commit_on_success(MySession, auto_flush=True) as s:
            assert s.autoflush == True
