from typing import List


class SeriesSearchData(object):
    def __init__(self,
                 aliases: List[str] = None,
                 banner: str = None,
                 firstAired: str = None,
                 id: int = None,
                 network: str = None,
                 overview: str = None,
                 seriesName: str = None,
                 status: str = None
                 ):
        self.status = status
        self.seriesName = seriesName
        self.overview = overview
        self.network = network
        self.id = id
        self.firstAired = firstAired
        self.banner = banner
        if aliases is None:
            aliases = []
        self.aliases = aliases
