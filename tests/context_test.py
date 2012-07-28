import unittest
import mock

from alchemytools.context import commit_on_success


class CommitOnSuccessTest(unittest.TestCase):

    def test_call_session_class(self):
        MySession = mock.Mock()
        with commit_on_success(MySession):
            assert MySession.call_count == 1
