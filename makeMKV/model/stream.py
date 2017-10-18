from enum import Enum

from makeMKV.model.enum import StreamFlags


class Type(Enum):
    VIDEO = 0
    AUDIO = 1
    SUBTITLES = 3


class Resolution(object):
    x: int
    y: int

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class AspectRatio(object):
    x: int
    y: int

    def __init__(self, x=0, y=0, input=None):
        if input != None and type(input) == str:
            (self.x, self.y) = input.split(':')
        else:
            self.x = x
            self.y = y


class Stream(object):
    type: Type
    codec_id: str
    codec_short: str
    codec_long: str
    stream_flags: StreamFlags
    mata_data_language_code: str
    meta_data_language_name: str
    tree_info: str
    panel_info: str
    order_weight: int
    mkv_flags: int
    mkv_flags_text: str

    def __init__(self,
                 type: Type = None,
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
        self.mata_data_language_code = mata_data_language_code
        self.meta_data_language_name = meta_data_language_name
        self.tree_info = tree_info
        self.panel_info = panel_info
        self.order_weight = order_weight
        self.mkv_flags = mkv_flags
        self.mkv_flags_text = mkv_flags_text


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
        super().__init__(Type.VIDEO,
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
        super().__init__(Type.AUDIO,
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
        self.name: str = name,
        self.language_code: str = language_code,
        self.language_name: str = language_name,
        self.bit_rate: int = bit_rate,
        self.audio_channel_count: int = audio_channel_count,
        self.audio_sample_rate: int = audio_sample_rate,
        self.volume_name: str = volume_name,
        self.audio_channel_layout_name: str = audio_channel_layout_name,
        self.output_conversion_type: str = output_conversion_type,


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
                 name: str = None,
                 language_code: str = None,
                 language_name: str = None):
        super().__init__(Type.SUBTITLES,
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
