import unittest

from commander import MockCommander
from handbrakeCLI.handbrakeCLI_impl import HandbrakeCLI


class TestHandbrakeCLI(unittest.TestCase):
    def test_compress_file(self):
        handbrakeCLI: HandbrakeCLI = HandbrakeCLI(MockCommander(0, './compressFile/std_out', './compressFile/std_err'))

        handbrakeCLI.compressFile('test', 'test')
