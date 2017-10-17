from enum import Enum


class Info(Enum):
    UNKNOWN = 0
    TYPE = 1
    TITLE = 2
    LANG_CODE = 3
    LANG = 4
    CODEC_ID = 5
    CODEC_SHORT = 6
    CODEC_LONG = 7
    CHAPTERS = 8
    DURATION = 9
    SIZE = 10
    BYTES = 11
    EXTENSION = 12
    BITRATE = 13
    AUDIO_CHANNELS = 14
    ANGLE_INFO = 15
    FNAME = 16
    SAMPLE_RATE = 17
    SAMPLE_SIZE = 18
    VIDEO_SIZE = 19
    ASPECT_RATIO = 20
    FRAME_RATE = 21
    STREAM_FLAGS = 22
    DATE_TIME = 23
    TITLE_ID = 24
    SEGMENT_COUNT = 25
    SEGMENT_MAP = 26
    FILENAME = 27

    ORDER = 33


def fromString(input: str) -> Info:
    if int(input) == 0:
        return Info.UNKNOWN
    elif int(input) == 1:
        return Info.TYPE
    elif int(input) == 2:
        return Info.TITLE
    elif int(input) == 3:
        return Info.LANG_CODE
    elif int(input) == 4:
        return Info.LANG
    elif int(input) == 5:
        return Info.CODEC_ID
    elif int(input) == 6:
        return Info.CODEC_SHORT
    elif int(input) == 7:
        return Info.CODEC_LONG
    elif int(input) == 8:
        return Info.CHAPTERS
    elif int(input) == 9:
        return Info.DURATION
    elif int(input) == 0:
        return Info.SIZE
    elif int(input) == 1:
        return Info.BYTES
    elif int(input) == 2:
        return Info.EXTENSION
    elif int(input) == 3:
        return Info.BITRATE
    elif int(input) == 4:
        return Info.AUDIO_CHANNELS
    elif int(input) == 5:
        return Info.ANGLE_INFO
    elif int(input) == 6:
        return Info.FNAME
    elif int(input) == 7:
        return Info.SAMPLE_RATE
    elif int(input) == 8:
        return Info.SAMPLE_SIZE
    elif int(input) == 9:
        return Info.VIDEO_SIZE
    elif int(input) == 0:
        return Info.ASPECT_RATIO
    elif int(input) == 1:
        return Info.FRAME_RATE
    elif int(input) == 2:
        return Info.STREAM_FLAGS
    elif int(input) == 3:
        return Info.DATE_TIME
    else:
        raise Exception('Unknown Info Code: ' + input)
