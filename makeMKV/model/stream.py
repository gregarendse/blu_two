from makeMKV.model.aspect_ratio import AspectRatio
from makeMKV.model.enum import StreamFlags, ItemAttributeId
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
    panel_info: str
    order_weight: int
    mkv_flags: int
    mkv_flags_text: str

    def __init__(self,
                 type: StreamType = None,
                 codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_info: str = None,
                 order_weight: int = None,
                 mkv_flags: int = None,
                 mkv_flags_text: str = None):
        self.type = type
        self.codec_id = codec_id
        self.codec_short = codec_short
        self.codec_long = codec_long
        self.stream_flags = stream_flags
        self.meta_data_language_code = mata_data_language_code
        self.meta_data_language_name = meta_data_language_name
        self.tree_info = tree_info
        self.panel_info = panel_info
        self.order_weight = order_weight
        self.mkv_flags = mkv_flags
        self.mkv_flags_text = mkv_flags_text

    def setAttribute(self, attributeId: ItemAttributeId, value: str):
        value = str(value).strip(' \"\'')
        if ItemAttributeId.Type == attributeId:
            self.type = StreamType.of(str(value).upper())
        elif ItemAttributeId.CodecId == attributeId:
            self.codec_id = value
        elif ItemAttributeId.CodecShort == attributeId:
            self.codec_short = value
        elif ItemAttributeId.CodecLong == attributeId:
            self.codec_long = value
        elif ItemAttributeId.StreamFlags == attributeId:
            self.stream_flags = StreamFlags(value)
        elif ItemAttributeId.MetadataLanguageCode == attributeId:
            self.meta_data_language_code = value
        elif ItemAttributeId.MetadataLanguageName == attributeId:
            self.meta_data_language_name = value
        elif ItemAttributeId.TreeInfo == attributeId:
            self.tree_info = value
        elif ItemAttributeId.PanelTitle == attributeId:
            self.panel_info = value
        elif ItemAttributeId.OrderWeight == attributeId:
            self.order_weight = int(value)
        elif ItemAttributeId.MkvFlags == attributeId:
            self.mkv_flags = int(value)
        elif ItemAttributeId.MkvFlagsText == attributeId:
            self.mkv_flags_text = value
        else:
            raise Exception("Invalid Attribute Id: " + str(attributeId))


class VideoStream(Stream):
    video_size: Resolution
    aspect_ratio: AspectRatio
    frame_rate: float

    def __init__(self, codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_info: str = None,
                 order_weight: int = None,
                 mkv_flags: int = None,
                 mkv_flags_text: str = None,
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
                         panel_info=panel_info,
                         order_weight=order_weight,
                         mkv_flags=mkv_flags,
                         mkv_flags_text=mkv_flags_text)
        self.video_size = video_size
        self.aspect_ratio = aspect_ratio
        self.frame_rate = frame_rate

    def setAttribute(self, attributeId: ItemAttributeId, value: str):
        value = str(value).strip(' \'\"')
        if ItemAttributeId.VideoSize == attributeId:
            parts = value.split('x')
            self.video_size = Resolution(int(parts[0]), int(parts[1]))
        elif ItemAttributeId.VideoAspectRatio == ItemAttributeId:
            parts = value.split(':')
            self.aspect_ratio = AspectRatio(int(parts[0]), int(parts[1]))
        elif ItemAttributeId.VideoFrameRate == attributeId:
            self.frame_rate = float(value)
        else:
            super().setAttribute(attributeId, value)


class AudioStream(Stream):
    name: str
    language_code: str
    language_name: str
    bit_rate: int
    audio_channel_count: int
    audio_sample_rate: int
    volume_name: str
    audio_channel_layout_name: str
    output_conversion_type: str

    def __init__(self,
                 codec_id: str = None,
                 codec_short: str = None,
                 codec_long: str = None,
                 stream_flags: StreamFlags = None,
                 mata_data_language_code: str = None,
                 meta_data_language_name: str = None,
                 tree_info: str = None,
                 panel_info: str = None,
                 order_weight: int = None,
                 mkv_flags: int = None,
                 mkv_flags_text: str = None,
                 name: str = None,
                 language_code: str = None,
                 language_name: str = None,
                 bit_rate: int = None,
                 audio_channel_count: int = None,
                 audio_sample_rate: int = None,
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
                         panel_info=panel_info,
                         order_weight=order_weight,
                         mkv_flags=mkv_flags,
                         mkv_flags_text=mkv_flags_text)
        self.name: str = name
        self.language_code: str = language_code
        self.language_name: str = language_name
        self.bit_rate: int = bit_rate
        self.audio_channel_count: int = audio_channel_count
        self.audio_sample_rate: int = audio_sample_rate
        self.volume_name: str = volume_name
        self.audio_channel_layout_name: str = audio_channel_layout_name
        self.output_conversion_type: str = output_conversion_type

    def setAttribute(self, attributeId: ItemAttributeId, value: str):
        if ItemAttributeId.Name == attributeId:
            self.name = value
        elif ItemAttributeId.LangCode == attributeId:
            self.language_code = value
        elif ItemAttributeId.LangName == attributeId:
            self.language_name = value
        elif ItemAttributeId.BitRate == attributeId:
            self.bit_rate = int(value)
        elif ItemAttributeId.AudioChannelsCount == attributeId:
            self.audio_channel_count = int(value)
        elif ItemAttributeId.AudioSampleRate == attributeId:
            self.audio_sample_rate = int(value)
        elif ItemAttributeId.VolumeName == attributeId:
            self.volume_name = value
        elif ItemAttributeId.AudioChannelLayoutName == attributeId:
            self.audio_channel_layout_name = value
        elif ItemAttributeId.OutputConversionType == attributeId:
            self.output_conversion_type = value
        else:
            super().setAttribute(attributeId, value)


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
                 panel_info: str = None,
                 order_weight: int = None,
                 mkv_flags: int = None,
                 mkv_flags_text: str = None,
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
                         panel_info=panel_info,
                         order_weight=order_weight,
                         mkv_flags=mkv_flags,
                         mkv_flags_text=mkv_flags_text)
        self.language_code: str = language_code
        self.language_name: str = language_name

    def setAttribute(self, attributeId: ItemAttributeId, value: str):
        if ItemAttributeId.LangCode == attributeId:
            self.language_code = value
        elif ItemAttributeId.LangName == attributeId:
            self.language_name = value
        else:
            super().setAttribute(attributeId, value)
