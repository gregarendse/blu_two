from enum import Enum
from typing import List

from commander import Commander, Response
from makeMKV.model import Drive
from makeMKV.model.disc import Disc
from makeMKV.model.enum import DriveState, DiskMediaFlag


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


def fromString(input: str) -> Type:
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


class MakeMKV(object):
    def __init__(self, commander: Commander):
        self.min_length = 900
        self.commander: Commander = commander
        self.executable: str = 'makemkvcon.exe'

    def scan_drives(self) -> List[Drive]:
        response: Response = self.commander.call('{executable} -r info disc:-1'.format(executable=self.executable))

        if response.return_code != 0:
            raise Exception(response.std_err)

        return self.__parse_scan_drives_output__(response.std_out)

    def scan_disc(self, drive: Drive) -> Disc:
        response: Response = self.commander.call(
            '{executable} -r info disc:{disc} --minlength={min_length} --noscan'
                .format(executable=self.executable, disc=drive.index, min_length=self.min_length))

        if response.return_code != 0:
            raise Exception(response.std_err)

        return self.__parse_scan_disc_output__(response.std_out)

    def __parse_scan_drives_output__(self, std_out: List[str]) -> List[Drive]:
        drives: List[Drive] = []
        for line in std_out:
            if len(line) == 0:
                continue

            (type, values) = line.split(':', maxsplit=1)
            line_type: Type = Type(fromString(type))
            line_parts: List[str] = values.split(',')

            if Type.MSG == line_type:
                pass
            elif Type.PRGC == line_type:
                pass
            elif Type.PRGT == line_type:
                pass
            elif Type.PRGV == line_type:
                pass
            elif Type.DRV == line_type:
                if len(line_parts) < 6:
                    raise Exception('Expected 6 parts to a \"DRV\" line!', line_parts)

                drive: Drive = Drive(
                    index=int(line_parts[0]),
                    visible=DriveState(int(line_parts[1])),
                    flags=DiskMediaFlag(int(line_parts[3])),
                    drive_name=line_parts[4].strip('\"'),
                    disc_name=line_parts[5].strip('\"')
                )

                if drive.visible:
                    drives.append(drive)

            elif Type.TCOUNT == line_type:
                pass
            elif Type.CINFO == line_type:
                pass
            elif Type.TINFO == line_type:
                pass
            elif Type.SINFO == line_type:
                pass
            else:
                raise Exception('How did we get here?')

        return [drive for drive in drives if drive.visible == DriveState.Inserted]

    def __parse_scan_disc_output__(self, std_out: List[str]) -> Disc:
        disc: Disc = Disc()
        for line in std_out:
            if len(line) == 0:
                continue

            (type, values) = line.split(':', maxsplit=1)
            line_type: Type = Type(fromString(type))

            if Type.MSG == line_type:
                pass
            elif Type.PRGC == line_type:
                pass
            elif Type.PRGT == line_type:
                pass
            elif Type.PRGV == line_type:
                pass
            elif Type.DRV == line_type:
                pass
            elif Type.TCOUNT == line_type:
                pass
            elif Type.CINFO == line_type:
                disc.setAttribute(values)
            elif Type.TINFO == line_type:
                disc.setTitleAttribute(values)
            elif Type.SINFO == line_type:
                pass
            else:
                raise Exception('How did we get here?')

        return disc
