from enum import Enum


class ItemAttributeId(Enum):
    """
    Derived from makemkvgui/inc/lgpl/apdefs.h
    """
    Unknown = 0
    Type = 1
    Name = 2
    LangCode = 3
    LangName = 4
    CodecId = 5
    CodecShort = 6
    CodecLong = 7
    ChapterCount = 8
    Duration = 9
    DiskSize = 10
    DiskSizeBytes = 11
    StreamTypeExtension = 12
    BitRate = 13
    AudioChannelsCount = 14
    AngleInfo = 15
    SourceFileName = 16
    AudioSampleRate = 17
    AudioSampleSize = 18
    VideoSize = 19
    VideoAspectRatio = 20
    VideoFrameRate = 21
    StreamFlags = 22
    DateTime = 23
    OriginalTitleId = 24
    SegmentsCount = 25
    SegmentsMap = 26
    OutputFileName = 27
    MetadataLanguageCode = 28
    MetadataLanguageName = 29
    TreeInfo = 30
    PanelTitle = 31
    VolumeName = 32
    OrderWeight = 33
    OutputFormat = 34
    OutputFormatDescription = 35
    SeamlessInfo = 36
    PanelText = 37
    MkvFlags = 38
    MkvFlagsText = 39
    AudioChannelLayoutName = 40
    OutputCodecShort = 41
    OutputConversionType = 42
    OutputAudioSampleRate = 43
    OutputAudioSampleSize = 44
    OutputAudioChannelsCount = 45
    OutputAudioChannelLayoutName = 46
    OutputAudioChannelLayout = 47
    OutputAudioMixDescription = 48
    Comment = 49
    OffsetSequenceId = 50
