from enum import Enum


class DiscType(Enum):
    DVD_TYPE_DISK = 6206
    BRAY_TYPE_DISK = 6209
    HDDVD_TYPE_DISK = 6212

    def toString(self) -> str:
        if self.value == 6206:
            return 'DVD'
        elif self.value == 6209:
            return 'BLURAY'
        elif self.value == 6212:
            return 'HDDVD'
