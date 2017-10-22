from enum import Enum


class StreamType(Enum):
    TITLE = 6200
    VIDEO = 6201
    AUDIO = 6202
    SUBTITLES = 6203

    def of(input: str):
        if input.upper() == 'VIDEO':
            return StreamType.VIDEO
        elif input.upper() == 'AUDIO':
            return StreamType.AUDIO
        elif input.upper() == 'SUBTITLES':
            return StreamType.SUBTITLES
        else:
            raise Exception('Invalid Input: ' + input)