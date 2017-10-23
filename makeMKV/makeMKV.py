import os
from enum import Enum
from typing import List, Dict, Optional

from commander import Commander, Response
from makeMKV.model.disc import Disc
from makeMKV.model.drive import Drive
from makeMKV.model.enum.disk_media_flag import DiskMediaFlag
from makeMKV.model.enum.drive_state import DriveState
from makeMKV.model.enum.item_attribute_id import ItemAttributeId
from makeMKV.model.title import Title


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

    def rip_disc(self, drive: Drive, destinationFolder: str, titleId: str = 'all') -> Optional[str]:
        response: Response = self.commander.call(
            '{executable} -r mkv disc:{discId} {titleId} {destinationFolder} --minlength={minLength} --noscan'
                .format(executable=self.executable, discId=drive.index, titleId=titleId,
                        destinationFolder=destinationFolder, minLength=self.min_length))

        if response.return_code != 0:
            raise Exception(response.std_out)

        if drive.disc.titles.get(titleId) != None:
            return os.path.join(destinationFolder, drive.disc.titles[titleId])
        else:
            return destinationFolder

    def scan_disc(self, drive: Drive) -> Drive:
        response: Response = self.commander.call(
            '{executable} -r info disc:{disc} --minlength={min_length} --noscan'
                .format(executable=self.executable, disc=drive.index, min_length=self.min_length))

        if response.return_code != 0:
            raise Exception(response.std_err)

        drive.disc = self.__parse_scan_disc_output__(response.std_out)

        return drive

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
            parts: List[str] = values.split(',', maxsplit=2)

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
                disc.setAttribute(
                    attributeId=ItemAttributeId(int(parts[0])),
                    code=int(parts[1]),
                    value=str(parts[2]).strip('\"')
                )
            elif Type.TINFO == line_type:
                sub_parts: List[str] = str(parts[2]).split(',', maxsplit=1)
                disc.setTitleAttribute(
                    titleId=int(parts[0]),
                    attributeId=ItemAttributeId(int(parts[1])),
                    code=int(sub_parts[0]),
                    value=str(sub_parts[1]).strip('\"')
                )
            elif Type.SINFO == line_type:
                sub_parts: List[str] = str(parts[2]).split(',', maxsplit=2)
                disc.setStreamAttribute(
                    titleId=int(parts[0]),
                    streamId=int(parts[1]),
                    attributeId=ItemAttributeId(int(sub_parts[0])),
                    code=int(sub_parts[1]),
                    value=str(sub_parts[2]).strip('\"')
                )
            else:
                raise Exception('How did we get here?')

        return self.__filter_scan_disc_output__(disc)

    def __filter_scan_disc_output__(self, disc: Disc) -> Disc:
        title_map: Dict[int, Title] = {}
        for key, value in disc.titles.items():
            if title_map.get(value.segments_map) == None:
                title_map[value.segments_map] = value
            elif title_map.get(value.segments_map).compare(value) < 0:
                title_map[value.segments_map] = value
        disc.titles = title_map

        return disc
