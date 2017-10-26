from enum import Enum


class Type(Enum):
    MSG = 0  # Message output
    PRGC = 1  # Current progress title
    PRGT = 2  # Total progress title
    PRGV = 3  # Progress bar values for current and total progress
    DRV = 4  # Drive scan messages
    TCOUNT = 5  # Disc information - Title count
    CINFO = 6  # Disc Information
    TINFO = 7  # Title Information
    SINFO = 8  # Stream Information

    def fromString(input: str):
        if input == 'MSG':
            return Type.MSG
        elif input == 'PRGC':
            return Type.PRGC
        elif input == 'PRGT':
            return Type.PRGT
        elif input == 'PRGV':
            return Type.PRGV
        elif input == 'DRV':
            return Type.DRV
        elif input == 'TCOUNT':
            return Type.TCOUNT
        elif input == 'CINFO':
            return Type.CINFO
        elif input == 'TINFO':
            return Type.TINFO
        elif input == 'SINFO':
            return Type.SINFO
        else:
            raise Exception('Unknown type: ' + input)
