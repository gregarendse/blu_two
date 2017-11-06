import unittest

from identifier.identifier_impl import Identifier


class TestIdentifier(unittest.TestCase):
    def test_identify(self):
        identifier = Identifier()

        result = identifier.identify('Friends Season 10 Disc 1')
