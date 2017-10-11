import unittest

from commander import MockCommander, Response


class TestMockCommander(unittest.TestCase):
    def test_call(self):
        commander = MockCommander(32, 'std_out.txt', 'std_err.txt')

        result: Response = commander.call('test')

        self.assertEqual(32, result.return_code)
        self.assertEqual(['std_out', ''], result.std_out)
        self.assertEqual(['std_err', ''], result.std_err)


if __name__ == '__main__':
    unittest.main()
