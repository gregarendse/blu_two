import unittest
from typing import List

from commander import MockCommander
from makeMKV.makeMKV import MakeMKV
from makeMKV.model.disc import Disc
from makeMKV.model.drive import Drive
from makeMKV.model.enum.disc_type import DiscType
from makeMKV.model.enum.disk_media_flag import DiskMediaFlag
from makeMKV.model.enum.drive_state import DriveState
from makeMKV.model.enum.item_info import ItemInfo
from makeMKV.model.enum.stream_flags import StreamFlags
from makeMKV.model.enum.stream_type import StreamType
from makeMKV.model.stream import VideoStream, AudioStream, SubtitleStream
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

        makeMKV.scan_disc(drive)

        disc: Disc = drive.disc

        self.assertEqual(DiscType.BRAY_TYPE_DISK, disc.type)
        self.assertEqual('Friends Season 10 Disc 1', disc.name)
        self.assertEqual('eng', disc.meta_language_code)
        self.assertEqual('English', disc.meta_language_name)
        self.assertEqual('Friends Season 10 Disc 1', disc.tree_info)
        self.assertEqual(ItemInfo.SOURCE, disc.panel_title)
        self.assertEqual('FRIENDS_S10', disc.volume_name)
        self.assertEqual(0, disc.order_weight)

        self.assertGreater(len(disc.titles), 0)

        title: Title = disc.titles[71]

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

        self.assertGreater(len(title.streams), 0)

        video: VideoStream = title.streams[0]

        self.assertEqual(StreamType.VIDEO, video.type)
        self.assertEqual('V_MPEG4/ISO/AVC', video.codec_id)
        self.assertEqual('Mpeg4', video.codec_short)
        self.assertEqual('Mpeg4', video.codec_long)
        self.assertEqual(StreamFlags(), video.stream_flags)
        self.assertEqual('eng', video.meta_data_language_code)
        self.assertEqual('English', video.meta_data_language_name)
        self.assertEqual('Mpeg4', video.tree_info)
        self.assertEqual(ItemInfo.TRACK, video.panel_title)
        self.assertEqual(0, video.order_weight)
        self.assertEqual(None, video.mkv_flags)
        self.assertEqual(None, video.mkv_flags_text)
        self.assertEqual('( Lossless conversion )', video.output_conversion_type)
        self.assertEqual(1920, video.video_size.x)
        self.assertEqual(1080, video.video_size.y)
        self.assertEqual(16, video.aspect_ratio.x)
        self.assertEqual(9, video.aspect_ratio.y)
        self.assertEqual(23.976, video.frame_rate)

        audio: AudioStream = title.streams[1]

        self.assertEqual(StreamType.AUDIO, audio.type)
        self.assertEqual('Surround 5.1', audio.name)
        self.assertEqual('eng', audio.meta_data_language_code)
        self.assertEqual('English', audio.meta_data_language_name)
        self.assertEqual('A_AC3', audio.codec_id)
        self.assertEqual('DD', audio.codec_short)
        self.assertEqual('Dolby Digital', audio.codec_long)
        self.assertEqual(640, audio.bit_rate)
        self.assertEqual(6, audio.audio_channel_count)
        self.assertEqual(48000, audio.audio_sample_rate)
        self.assertEqual(StreamFlags(), audio.stream_flags)
        self.assertEqual('eng', audio.language_code)
        self.assertEqual('English', audio.language_name)
        self.assertEqual('DD Surround 5.1 English', audio.tree_info)
        self.assertEqual(ItemInfo.TRACK, audio.panel_title)
        self.assertEqual(90, audio.order_weight)
        self.assertEqual('d', audio.mkv_flags)
        self.assertEqual('Default', audio.mkv_flags_text)
        self.assertEqual('5.1(side)', audio.audio_channel_layout_name)
        self.assertEqual('( Lossless conversion )', audio.output_conversion_type)

        subtitle: SubtitleStream = title.streams[6]

        self.assertEqual(StreamType.SUBTITLES, subtitle.type)
        self.assertEqual('S_HDMV/PGS', subtitle.codec_id)
        self.assertEqual('PGS', subtitle.codec_short)
        self.assertEqual('HDMV PGS Subtitles', subtitle.codec_long)
        self.assertEqual(StreamFlags(), subtitle.stream_flags)
        self.assertEqual('eng', subtitle.meta_data_language_code)
        self.assertEqual('English', subtitle.meta_data_language_name)
        self.assertEqual('PGS English', subtitle.tree_info)
        self.assertEqual(ItemInfo.TRACK, subtitle.panel_title)
        self.assertEqual(90, subtitle.order_weight)
        self.assertEqual(None, subtitle.mkv_flags)
        self.assertEqual(None, subtitle.mkv_flags_text)
        self.assertEqual('( Lossless conversion )', subtitle.output_conversion_type)
        self.assertEqual('eng', subtitle.language_code)
        self.assertEqual('English', subtitle.language_name)

    def test_rip_disc(self):
        makeMKV: MakeMKV = MakeMKV(
            MockCommander(0, './rip_title/std_out', './rip_title/std_err')
        )

        mock_drive: Drive = Drive()
        mock_drive.index = 0
        mock_drive.disc = Disc()
        mock_drive.disc.titles = {}
        mock_drive.disc.titles[0] = Title(0)
        mock_drive.disc.titles[0].output_file_name = 'test'

        output: str = makeMKV.rip_disc(mock_drive, 'dest', 0)

        self.assertEqual('dest\\test', output)
