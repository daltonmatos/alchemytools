import unittest
import mock

from alchemytools.context import managed
from alchemytools.callback import Callback


class BaseDumbSession(object):

    def commit(self):
        pass

    def close(self):
        pass

    def rollback(self):
        pass


class ManagedAsContextManagerTest(unittest.TestCase):

    def setUp(self):
        self.mock_session = mock.Mock()

    def test_call_session_class(self):
        with managed(self.mock_session):
            self.assertEqual(self.mock_session.call_count, 1)

    def test_set_autoflush_default_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = True

        with managed(MySession) as s:
            self.assertFalse(s.autoflush)

    def test_set_autoflush_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = False

        with managed(MySession, auto_flush=True) as s:
            self.assertTrue(s.autoflush)

    def test_set_autocommit_false(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autocommit = True

        with managed(MySession) as s:
            self.assertFalse(s.autocommit)

    def test_set_autocommit_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autocommit = False

        with managed(MySession, auto_commit=True) as s:
            self.assertTrue(s.autocommit)

    def test_commit_after_yield_when_commit_on_success_is_default(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with managed(self.mock_session):
            pass
        self.assertEqual(real_session.commit.call_count, 1)

    def test_dont_commit_after_yield_when_commit_on_success_is_false(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with managed(self.mock_session, commit_on_success=False):
            pass
        self.assertEqual(real_session.commit.call_count, 0)

    def test_close_after_yield(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        with managed(self.mock_session):
            pass
        self.assertEqual(real_session.close.call_count, 1)

    def test_rollback_on_exception(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        try:
            with managed(self.mock_session):
                raise Exception()
        except:
            pass
        self.assertEqual(real_session.rollback.call_count, 1)
        self.assertEqual(real_session.commit.call_count, 0)
        self.assertEqual(real_session.close.call_count, 1)

    def test_context_should_reraise_exceptions(self):
        raised = False
        try:
            with managed(mock.Mock()):
                raise Exception()
        except:
            raised = True
        self.assertTrue(raised)

    def test_callback_is_called(self):
        func = mock.Mock()
        callback = Callback(func, 42, foo="bar")
        try:
            with managed(mock.Mock(), callback=callback):
                raise Exception
        except:
            func.assert_called_once_with(42, foo="bar")

    def test_session_is_closed_on_return(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session

        def func():
            with managed(self.mock_session):
                return False

        func()

        self.assertEqual(real_session.close.call_count, 1)


class ManagedAsDecorator(unittest.TestCase):

    def setUp(self):
        self.mock_session = mock.Mock()

        def f(session):
            pass

        self.f = f

    def test_call_session_class(self):
        f = managed(self.mock_session)(self.f)
        f()
        self.assertEqual(self.mock_session.call_count, 1)

    def test_set_autoflush_default_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = True

        @managed(MySession)
        def f(s):
            self.assertFalse(s.autoflush)

        f()

    def test_set_autoflush_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autoflush = False

        @managed(MySession, auto_flush=True)
        def f(s):
            self.assertTrue(s.autoflush)

        f()

    def test_set_autocommit_false(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autocommit = True

        @managed(MySession)
        def f(s):
            self.assertFalse(s.autocommit)

        f()

    def test_set_autocommit_value(self):
        class MySession(BaseDumbSession):
            def __init__(self):
                self.autocommit = False

        @managed(MySession, auto_commit=True)
        def f(s):
            self.assertTrue(s.autocommit)

        f()

    def test_commit_if_success_when_commit_on_success_is_default(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session

        f = managed(self.mock_session)(self.f)
        f()
        self.assertEqual(real_session.commit.call_count, 1)

    def test_dont_commit_if_success_when_commit_on_success_is_false(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        f = managed(self.mock_session, commit_on_success=False)(self.f)
        f()
        self.assertEqual(real_session.commit.call_count, 0)

    def test_close_when_success(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        f = managed(self.mock_session)(self.f)
        f()
        self.assertEqual(real_session.close.call_count, 1)

    def test_rollback_on_exception(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session
        raised = False

        @managed(self.mock_session)
        def f(s):
            raise Exception()

        try:
            f()
        except Exception as e:
            raised = True

        self.assertTrue(raised)
        self.assertEqual(real_session.rollback.call_count, 1)
        self.assertEqual(real_session.commit.call_count, 0)
        self.assertEqual(real_session.close.call_count, 1)

    def test_callback_is_called_when_failed(self):
        func = mock.Mock()
        callback = Callback(func, 42, f="bar")

        @managed(self.mock_session, callback=callback)
        def f(s):
            raise Exception()

        try:
            f()
        except Exception as e:
            pass

        self.assertEqual(func.call_args_list, [mock.call(42, f='bar')])

    def test_session_is_closed_on_return(self):
        real_session = mock.Mock()
        self.mock_session.return_value = real_session

        f = managed(self.mock_session)(self.f)
        f()

        self.assertEqual(real_session.close.call_count, 1)


if __name__ == "__main__":
    unittest.main()
