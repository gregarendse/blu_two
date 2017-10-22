from enum import Enum


class StreamType(Enum):
    VIDEO = 0
    AUDIO = 1
    SUBTITLES = 3

    def of(input: str):
        if input.upper() == 'VIDEO':
            return StreamType.VIDEO
        elif input.upper() == 'AUDIO':
            return StreamType.AUDIO
        elif input.upper() == 'SUBTITLES':
            return StreamType.SUBTITLES
        else:
            raise Exception('Invalid Input: ' + input)