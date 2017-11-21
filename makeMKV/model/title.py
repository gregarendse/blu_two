from typing import Dict

from makeMKV.model.enum.item_attribute_id import ItemAttributeId
from makeMKV.model.enum.item_info import ItemInfo
from makeMKV.model.enum.stream_type import StreamType
from makeMKV.model.stream import Stream, VideoStream, SubtitleStream, AudioStream


class Title(object):
    id: int
    name: str
    chapters: int
    duration: int
    bytes: int
    source_file_name: str
    segments_count: int
    segments_map: int
    output_file_name: str
    metadata_language_code: str
    metadata_language_name: str
    tree_info: str
    panel_title: ItemInfo
    order_weight: int
    raw_location: str

    streams: Dict[int, Stream]

    def __init__(self,
                 id: int,
                 name=None,
                 chapters=None,
                 duration=None,
                 bytes=None,
                 source_file_name=None,
                 segments_count=None,
                 segments_map=None,
                 output_file_name=None,
                 metadata_language_code=None,
                 metadata_language_name=None,
                 tree_info=None,
                 panel_title=None,
                 order_weight=None):
        self.id = id
        self.name = name
        self.chapters = chapters
        self.duration = duration
        self.bytes = bytes
        self.source_file_name = source_file_name
        self.segments_count = segments_count
        self.segments_map = segments_map
        self.output_file_name = output_file_name
        self.metadata_language_code = metadata_language_code
        self.metadata_language_name = metadata_language_name
        self.tree_info = tree_info
        self.panel_title = panel_title
        self.order_weight = order_weight
        self.raw_location = None

        self.streams = {}

        self.name: str = None
        self.episode: int = None
        self.season: int = None
        self.series: str = None

    def setAttribute(self, attributeId: ItemAttributeId, code: int, value: str) -> None:
        """
        TINFO:0,2,0,"Friends Season 10 Disc 1"
        TINFO:0,8,0,"4"
        TINFO:0,9,0,"0:22:56"
        TINFO:0,10,0,"2.9 GB"
        TINFO:0,11,0,"3130791936"
        TINFO:0,16,0,"00080.mpls"
        TINFO:0,25,0,"1"
        TINFO:0,26,0,"71"
        TINFO:0,27,0,"Friends_Season_10_Disc_1_t00.mkv"
        TINFO:0,28,0,"eng"
        TINFO:0,29,0,"English"
        TINFO:0,30,0,"Friends Season 10 Disc 1 - 4 chapter(s) , 2.9 GB"
        TINFO:0,31,6120,"<b>Title information</b><br>"
        TINFO:0,33,0,"0"
        :return:
        """

        if ItemAttributeId.Name == attributeId:
            self.name = str(value)
        elif ItemAttributeId.ChapterCount == attributeId:
            self.chapters = int(value)
        elif ItemAttributeId.Duration == attributeId:
            (hrs, min, sec) = str(value).split(':', 3)
            self.duration = (int(hrs) * 3600) + (int(min) * 60) + int(sec)
        elif ItemAttributeId.DiskSize == attributeId:
            pass
        elif ItemAttributeId.DiskSizeBytes == attributeId:
            self.bytes = int(value)
        elif ItemAttributeId.SourceFileName == attributeId:
            self.source_file_name = str(value)
        elif ItemAttributeId.SegmentsCount == attributeId:
            self.segments_count = int(value)
        elif ItemAttributeId.SegmentsMap == attributeId:
            self.segments_map = int(value)
        elif ItemAttributeId.OutputFileName == attributeId:
            self.output_file_name = str(value)
        elif ItemAttributeId.MetadataLanguageCode == attributeId:
            self.metadata_language_code = str(value)
        elif ItemAttributeId.MetadataLanguageName == attributeId:
            self.metadata_language_name = str(value)
        elif ItemAttributeId.TreeInfo == attributeId:
            self.tree_info = str(value)
        elif ItemAttributeId.PanelTitle == attributeId:
            self.panel_title = ItemInfo(int(code))
        elif ItemAttributeId.OrderWeight == attributeId:
            self.order_weight = int(value)
        else:
            raise Exception('Unknown attribute: {attributeId}, code: {code}, value: {value}'
                            .format(attributeId=attributeId, code=code, value=value))

    def setStreamAttribute(self, streamId: int, attributeId: ItemAttributeId, code: int, value: str) -> None:
        """
SINFO:0,0,1,6201,"Video"
SINFO:0,0,5,0,"V_MPEG4/ISO/AVC"
SINFO:0,0,6,0,"Mpeg4"
SINFO:0,0,7,0,"Mpeg4"
SINFO:0,0,19,0,"1920x1080"
SINFO:0,0,20,0,"16:9"
SINFO:0,0,21,0,"23.976 (24000/1001)"
SINFO:0,0,22,0,"0"
SINFO:0,0,28,0,"eng"
SINFO:0,0,29,0,"English"
SINFO:0,0,30,0,"Mpeg4"
SINFO:0,0,31,6121,"<b>Track information</b><br>"
SINFO:0,0,33,0,"0"
SINFO:0,0,38,0,""
SINFO:0,0,42,5088,"( Lossless conversion )"

        :param streamId:
        :param attributeId:
        :param code:
        :param value:
        :return:
        """

        if self.streams.get(streamId) == None:
            if ItemAttributeId.Type != attributeId:
                raise Exception(
                    'Unknown Stream Type: {streamId}, AttributeId: {attributeId}, Code: {code}, Value: {value}'
                        .format(streamId=streamId, attributeId=attributeId, code=code, value=value))
            else:
                stream_type: StreamType = StreamType(int(code))
                if StreamType.VIDEO == stream_type:
                    self.streams[streamId] = VideoStream()
                elif StreamType.AUDIO == stream_type:
                    self.streams[streamId] = AudioStream()
                elif StreamType.SUBTITLES == stream_type:
                    self.streams[streamId] = SubtitleStream()
                else:
                    raise Exception(
                        'Unknown Stream Type: {streamId}, AttributeId: {attributeId}, Code: {code}, Value: {value}'
                            .format(streamId=streamId, attributeId=attributeId, code=code, value=value))
        else:
            self.streams.get(streamId).setAttribute(attributeId, code, value)

    def compare(self, other) -> int:
        if type(self) != type(other):
            raise Exception('Type mismatch, self: {self}, other: {other}'
                            .format(self=self, other=other))

        score: int = 0

        score += self.getVideoStream().video_size.compare(other.getVideoStream().video_size)

        if len(self.streams) > len(other.streams):
            return 1
        else:
            return -1

    def getVideoStream(self) -> VideoStream:
        for key, value in self.streams.items():
            if type(value) is VideoStream:
                return value

    def getAudioStream(self) -> AudioStream:
        for key, value in self.streams.items():
            if (type(value) is AudioStream):
                if value.mkv_flags == 'd':
                    return value
