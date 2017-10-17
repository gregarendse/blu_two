from typing import Optional


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
    """
    index: int
    visible: bool
    enabled: bool
    flags: int
    drive_name: Optional[str]
    disc_name: Optional[str]

    def __init__(self,
                 index: int = 0,
                 visible: bool = False,
                 enabled: bool = False,
                 flags: int = 0,
                 drive_name: Optional[str] = None,
                 disc_name: Optional[str] = None):
        self.index = index
        self.visible = visible
        self.enabled = enabled
        self.flags = flags
        self.drive_name = drive_name
        self.disc_name = disc_name
