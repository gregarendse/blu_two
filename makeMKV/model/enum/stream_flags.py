from flags import Flags


class StreamFlags(Flags):
    DirectorsComments = 1
    AlternateDirectorsComments = 2
    ForVisuallyImpaired = 4
    CoreAudio = 256
    SecondaryAudio = 512
    HasCoreAudio = 1024
    DerivedStream = 2048
    ForcedSubtitles = 4096
    ProfileSecondaryStream = 16384
    OffsetSequenceIdPresent = 32768

