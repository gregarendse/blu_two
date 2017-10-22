import unittest

from makeMKV.model.enum import ItemAttributeId, StreamFlags
from makeMKV.model.enum.stream_type import StreamType
from makeMKV.model.stream import Stream


class TestModel(unittest.TestCase):
    def test_set_attribute(self):
        test_data = [
            [ItemAttributeId.Type, "VIDEO"],
            [ItemAttributeId.CodecId, "codec_id"],
            [ItemAttributeId.CodecShort, "codec_short"],
            [ItemAttributeId.CodecLong, "codec_long"],
            [ItemAttributeId.StreamFlags, str(StreamFlags.DerivedStream | StreamFlags.CoreAudio)],
            [ItemAttributeId.MetadataLanguageCode, "meta_data_language_code"],
            [ItemAttributeId.MetadataLanguageName, "meta_data_language_name"],
            [ItemAttributeId.TreeInfo, "tree_info"],
            [ItemAttributeId.PanelTitle, "panel_info"],
            [ItemAttributeId.OrderWeight, "50"],
            [ItemAttributeId.MkvFlags, "10"],
            [ItemAttributeId.MkvFlagsText, "mkv_flags_text"],
        ]

        stream: Stream = Stream()

        for item in test_data:
            stream.setAttribute(item[0], item[1])

        self.assertEquals(StreamType.VIDEO, stream.type)
        self.assertEquals("codec_id", stream.codec_id)
        self.assertEquals("codec_short", stream.codec_short)
        self.assertEquals("codec_long", stream.codec_long)
        self.assertEquals(StreamFlags.DerivedStream | StreamFlags.CoreAudio, stream.stream_flags)
        self.assertEquals("meta_data_language_code", stream.meta_data_language_code)
        self.assertEquals("meta_data_language_name", stream.meta_data_language_name)
        self.assertEquals("tree_info", stream.tree_info)
        self.assertEquals("panel_info", stream.panel_title)
        self.assertEquals(50, stream.order_weight)
        self.assertEquals(10, stream.mkv_flags)
        self.assertEquals("mkv_flags_text", stream.mkv_flags_text)
