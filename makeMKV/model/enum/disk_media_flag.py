from flags import Flags


class DiskMediaFlag(Flags):
    """
    Derived from makemkvgui/inc/lgpl/apdefs.h
    """
    DVD = 1
    HD_DVD = 2
    BLURAY = 4
    AACS = 8
    BDSVM = 16
