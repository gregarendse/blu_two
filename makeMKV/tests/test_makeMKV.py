import unittest
from typing import List

from commander import MockCommander
from makeMKV import MakeMKV
from makeMKV.model import Drive


class TestMakeMKV(unittest.TestCase):
    def test_scan_drives(self):
        makeMKV: MakeMKV = MakeMKV(
            MockCommander(0, './scan_drives/std_out', './scan_drives/std_err')
        )

        drives: List[Drive] = makeMKV.scan_drives()

        self.assertEqual(1, len(drives))

        for drive in drives:
            self.assertEqual(0, drive.index)
            self.assertEqual(True, drive.enabled)
            self.assertEqual(True, drive.visible)
            self.assertEqual(12, drive.flags)
            self.assertEqual("BD-ROM HL-DT-ST BDDVDRW CH12NS30 1.02", drive.drive_name)
            self.assertEqual("FRIENDS_S10", drive.disc_name)
