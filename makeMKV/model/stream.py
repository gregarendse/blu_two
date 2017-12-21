from makeMKV.model.aspect_ratio import AspectRatio
from makeMKV.model.enum.item_attribute_id import ItemAttributeId
from makeMKV.model.enum.item_info import ItemInfo
from makeMKV.model.enum.stream_flags import StreamFlags
from makeMKV.model.enum.stream_type import StreamType
from makeMKV.model.resolution import Resolution


class Stream(object):
    type: StreamType
    codec_id: str
    codec_short: str
    codec_long: str
    stream_flags: StreamFlags
    meta_data_language_code: str
    meta_data_language_name: str
    tree_info: str
    panel_title: ItemInfo
    order_weight: int
    mkv_flags: str
    mkv_flags_text: str
    output_conversion_type: str

    def __init__(self,
                 type: StreamType = None,
                 codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_title: ItemInfo = None,
                 order_weight: int = None,
                 mkv_flags: str = None,
                 mkv_flags_text: str = None,
                 output_conversion_type: str = None):
        self.output_conversion_type: str = output_conversion_type
        self.type = type
        self.codec_id = codec_id
        self.codec_short = codec_short
        self.codec_long = codec_long
        self.stream_flags = stream_flags
        self.meta_data_language_code = mata_data_language_code
        self.meta_data_language_name = meta_data_language_name
        self.tree_info = tree_info
        self.panel_title = panel_title
        self.order_weight = order_weight
        self.mkv_flags = mkv_flags
        self.mkv_flags_text = mkv_flags_text
        self.output_conversion_type = output_conversion_type

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        if ItemAttributeId.Type == attributeId:
            self.type = StreamType.of(str(value).upper())
        elif ItemAttributeId.CodecId == attributeId:
            self.codec_id = value
        elif ItemAttributeId.CodecShort == attributeId:
            self.codec_short = value
        elif ItemAttributeId.CodecLong == attributeId:
            self.codec_long = value
        elif ItemAttributeId.StreamFlags == attributeId:
            self.stream_flags = StreamFlags(int(value))
        elif ItemAttributeId.MetadataLanguageCode == attributeId:
            self.meta_data_language_code = value
        elif ItemAttributeId.MetadataLanguageName == attributeId:
            self.meta_data_language_name = value
        elif ItemAttributeId.TreeInfo == attributeId:
            self.tree_info = value
        elif ItemAttributeId.PanelTitle == attributeId:
            self.panel_title = ItemInfo(int(code))
        elif ItemAttributeId.OrderWeight == attributeId:
            self.order_weight = int(value)
        elif ItemAttributeId.MkvFlags == attributeId:
            if len(value) > 0:
                self.mkv_flags = value
        elif ItemAttributeId.MkvFlagsText == attributeId:
            self.mkv_flags_text = value
        elif ItemAttributeId.OutputConversionType == attributeId:
            self.output_conversion_type = value
        elif ItemAttributeId.OutputFormat == attributeId:
            pass
        elif ItemAttributeId.OutputFormatDescription == attributeId:
            pass
        else:
            raise Exception('Unknown attribute: {attributeId}, code: {code}, value: {value}'
                            .format(attributeId=attributeId, code=code, value=value))


def compare(self, other) -> int:
    if type(other) != type(self):
        raise Exception('Type mismatch, self: {self}, other: {other}'
                        .format(self=self, other=other))

    return 0


class VideoStream(Stream):
    video_size: Resolution
    aspect_ratio: AspectRatio
    frame_rate: float

    def __init__(self,
                 codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_title: str = None,
                 order_weight: int = None,
                 mkv_flags: str = None,
                 mkv_flags_text: str = None,
                 output_conversion_type: str = None,
                 video_size: Resolution = None,
                 aspect_ratio: AspectRatio = None,
                 frame_rate: float = None):
        super().__init__(StreamType.VIDEO,
                         codec_id=codec_id,
                         codec_short=codec_short,
                         codec_long=codec_long,
                         stream_flags=stream_flags,
                         mata_data_language_code=mata_data_language_code,
                         meta_data_language_name=meta_data_language_name,
                         tree_info=tree_info,
                         panel_title=panel_title,
                         order_weight=order_weight,
                         mkv_flags=mkv_flags,
                         mkv_flags_text=mkv_flags_text,
                         output_conversion_type=output_conversion_type)
        self.video_size = video_size
        self.aspect_ratio = aspect_ratio
        self.frame_rate = frame_rate

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        if ItemAttributeId.VideoSize == attributeId:
            parts = str(value).split('x', maxsplit=1)
            self.video_size = Resolution(int(parts[0]), int(parts[1]))
        elif ItemAttributeId.VideoAspectRatio == attributeId:
            parts = str(value).split(':', maxsplit=1)
            self.aspect_ratio = AspectRatio(int(parts[0]), int(parts[1]))
        elif ItemAttributeId.VideoFrameRate == attributeId:
            self.frame_rate = float(
                str(value).split(' ')[0]
            )
        elif ItemAttributeId.BitRate == attributeId:
            pass
        else:
            super().setAttribute(attributeId, code, value)

    def compare(self, other):
        return self.video_size.compare(other.video_size)


class AudioStream(Stream):
    name: str
    language_code: str
    language_name: str
    bit_rate: int
    audio_channel_count: int
    audio_sample_rate: int
    audio_sample_size: int
    volume_name: str
    audio_channel_layout_name: str

    def __init__(self,
                 codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_title: str = None,
                 order_weight: int = None,
                 mkv_flags: str = None,
                 mkv_flags_text: str = None,
                 name: str = None,
                 language_code: str = None,
                 language_name: str = None,
                 bit_rate: int = None,
                 audio_channel_count: int = None,
                 audio_sample_rate: int = None,
                 audio_sample_size: int = None,
                 volume_name: str = None,
                 audio_channel_layout_name: str = None,
                 output_conversion_type: str = None):
        super().__init__(StreamType.AUDIO,
                         codec_id=codec_id,
                         codec_short=codec_short,
                         codec_long=codec_long,
                         stream_flags=stream_flags,
                         mata_data_language_code=mata_data_language_code,
                         meta_data_language_name=meta_data_language_name,
                         tree_info=tree_info,
                         panel_title=panel_title,
                         order_weight=order_weight,
                         mkv_flags=mkv_flags,
                         mkv_flags_text=mkv_flags_text,
                         output_conversion_type=output_conversion_type)
        self.name: str = name
        self.language_code: str = language_code
        self.language_name: str = language_name
        self.bit_rate: int = bit_rate
        self.audio_channel_count: int = audio_channel_count
        self.audio_sample_rate: int = audio_sample_rate
        self.audio_sample_size: int = audio_sample_size
        self.volume_name: str = volume_name
        self.audio_channel_layout_name: str = audio_channel_layout_name

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        if ItemAttributeId.Name == attributeId:
            self.name = value
        elif ItemAttributeId.LangCode == attributeId:
            self.language_code = value
        elif ItemAttributeId.LangName == attributeId:
            self.language_name = value
        elif ItemAttributeId.BitRate == attributeId:
            parts = value.split(' ')
            if parts[1] == 'Mb/s':
                self.bit_rate = int(float(parts[0]) * 1000)
            elif parts[1] == 'Kb/s':
                self.bit_rate = int(parts[0])
            else:
                raise Exception('Unhandled magnitude: ', parts[1])
        elif ItemAttributeId.AudioChannelsCount == attributeId:
            self.audio_channel_count = int(value)
        elif ItemAttributeId.AudioSampleRate == attributeId:
            self.audio_sample_rate = int(value)
        elif ItemAttributeId.AudioSampleSize == attributeId:
            self.audio_sample_size = int(value)
        elif ItemAttributeId.VolumeName == attributeId:
            self.volume_name = value
        elif ItemAttributeId.AudioChannelLayoutName == attributeId:
            self.audio_channel_layout_name = value
        else:
            super().setAttribute(attributeId, code, value)


class SubtitleStream(Stream):
    language_code: str
    language_name: str

    def __init__(self,
                 codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_title: str = None,
                 order_weight: int = None,
                 mkv_flags: str = None,
                 mkv_flags_text: str = None,
                 output_conversion_type: str = None,
                 language_code: str = None,
                 language_name: str = None):
        super().__init__(StreamType.SUBTITLES,
                         codec_id=codec_id,
                         codec_short=codec_short,
                         codec_long=codec_long,
                         stream_flags=stream_flags,
                         mata_data_language_code=mata_data_language_code,
                         meta_data_language_name=meta_data_language_name,
                         tree_info=tree_info,
                         panel_title=panel_title,
                         order_weight=order_weight,
                         mkv_flags=mkv_flags,
                         mkv_flags_text=mkv_flags_text,
                         output_conversion_type=output_conversion_type)
        self.language_code: str = language_code
        self.language_name: str = language_name

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        if ItemAttributeId.LangCode == attributeId:
            self.language_code = value
        elif ItemAttributeId.LangName == attributeId:
            self.language_name = value
        else:
            super().setAttribute(attributeId, code, value)
