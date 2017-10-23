from typing import Optional

from makeMKV.model.disc import Disc
from makeMKV.model.enum.disk_media_flag import DiskMediaFlag
from makeMKV.model.enum.drive_state import DriveState


class Drive(object):
    """
    Drive scan messages
    DRV:index,visible,enabled,flags,drive name,disc name
    index - drive index
    visible - set to 1 if drive is present
    enabled - set to 1 if drive is accessible
    flags - media flags, see AP_DskFsFlagXXX in apdefs.h
    drive name - drive name string
    disc name - disc name string
    http://www.makemkv.com/developers/usage.txt
    """
    index: int
    visible: DriveState
    flags: DiskMediaFlag
    drive_name: Optional[str]
    disc_name: Optional[str]
    disc: Disc

    def __init__(self,
                 index: int = None,
                 visible: DriveState = DriveState.NoDrive,
                 flags: DiskMediaFlag = None,
                 drive_name: Optional[str] = None,
                 disc_name: Optional[str] = None,
                 disc: Disc = None):
        self.index = index
        self.visible = visible
        self.flags = flags
        self.drive_name = drive_name
        self.disc_name = disc_name
        self.disc = disc
