import unittest
import mock

from alchemytools.callback import Callback


class CallbackTest(unittest.TestCase):
    def test_func_is_a_callable(self):
        func = "Not a function"
        self.assertRaises(TypeError, Callback, func)

    def test_func_is_called(self):
        func = mock.Mock()
        cb = Callback(func, 42, foo="bar")
        cb()
        func.assert_called_with(42, foo="bar")

    def test_func_should_not_raise_exception(self):
        func = mock.Mock()
        func.return_value = lambda: 0/0
        cb = Callback(func, 42)
        cb()
        func.assert_called_with(42)


if __name__ == "__main__":
    unittest.main()
