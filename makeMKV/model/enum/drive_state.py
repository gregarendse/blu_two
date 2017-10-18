from enum import Enum


class DriveState(Enum):
    EmptyClosed = 0
    EmptyOpen = 1
    Inserted = 2
    Loading = 3
    NoDrive = 256
    Unmounting = 257
