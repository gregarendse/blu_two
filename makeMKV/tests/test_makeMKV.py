import unittest
from typing import List

from commander import MockCommander
from makeMKV import MakeMKV
from makeMKV.model import Drive
from makeMKV.model.disc import Disc
from makeMKV.model.enum import DriveState, DiskMediaFlag
from makeMKV.model.enum.disc_type import DiscType
from makeMKV.model.enum.item_info import ItemInfo
from makeMKV.model.title import Title


class TestMakeMKV(unittest.TestCase):
    def test_scan_drives(self):
        makeMKV: MakeMKV = MakeMKV(
            MockCommander(0, './scan_drives/std_out', './scan_drives/std_err')
        )

        drives: List[Drive] = makeMKV.scan_drives()

        self.assertEqual(1, len(drives))

        for drive in drives:
            self.assertEqual(0, drive.index)
            self.assertEqual(DriveState.Inserted, drive.visible)
            self.assertEqual(DiskMediaFlag(12), drive.flags)
            self.assertEqual('BD-ROM HL-DT-ST BDDVDRW CH12NS30 1.02', drive.drive_name)
            self.assertEqual('FRIENDS_S10', drive.disc_name)

    def test_scan_disc(self):
        makeMKV: MakeMKV = MakeMKV(
            MockCommander(0, './scan_disc/std_out', './scan_disc/std_err')
        )

        drive: Drive = Drive(index=0)

        disc: Disc = makeMKV.scan_disc(drive)

        self.assertEqual(DiscType.BRAY_TYPE_DISK, disc.type)
        self.assertEqual('Friends Season 10 Disc 1', disc.name)
        self.assertEqual('eng', disc.meta_language_code)
        self.assertEqual('English', disc.meta_language_name)
        self.assertEqual('Friends Season 10 Disc 1', disc.tree_info)
        self.assertEqual(ItemInfo.SOURCE, disc.panel_title)
        self.assertEqual('FRIENDS_S10', disc.volume_name)
        self.assertEqual(0, disc.order_weight)

        self.assertGreater(len(disc.titles), 0)

        title: Title = disc.titles[0]

        self.assertEqual(0, title.id)
        self.assertEqual('Friends Season 10 Disc 1', title.name)
        self.assertEqual(4, title.chapters)
        self.assertEqual(1376, title.duration)
        self.assertEqual(3130791936, title.bytes)
        self.assertEqual('00080.mpls', title.source_file_name)
        self.assertEqual(1, title.segments_count)
        self.assertEqual(71, title.segments_map)
        self.assertEqual('Friends_Season_10_Disc_1_t00.mkv', title.output_file_name)
        self.assertEqual('eng', title.metadata_language_code)
        self.assertEqual('English', title.metadata_language_name)
        self.assertEqual('Friends Season 10 Disc 1 - 4 chapter(s) , 2.9 GB', title.tree_info)
        self.assertEqual(ItemInfo.TITLE, title.panel_title)
        self.assertEqual(0, title.order_weight)

# SINFO:0,0,1,6201,"Video"
# SINFO:0,0,5,0,"V_MPEG4/ISO/AVC"
# SINFO:0,0,6,0,"Mpeg4"
# SINFO:0,0,7,0,"Mpeg4"
# SINFO:0,0,19,0,"1920x1080"
# SINFO:0,0,20,0,"16:9"
# SINFO:0,0,21,0,"23.976 (24000/1001)"
# SINFO:0,0,22,0,"0"
# SINFO:0,0,28,0,"eng"
# SINFO:0,0,29,0,"English"
# SINFO:0,0,30,0,"Mpeg4"
# SINFO:0,0,31,6121,"<b>Track information</b><br>"
# SINFO:0,0,33,0,"0"
# SINFO:0,0,38,0,""
# SINFO:0,0,42,5088,"( Lossless conversion )"
