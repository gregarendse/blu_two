class BasicEpisode(object):
    def __init__(self,
                 absoluteNumber: str = None,
                 airedEpisodeNumber: str = None,
                 airedSeason: str = None,
                 dvdEpisodeNumber: str = None,
                 dvdSeason: str = None,
                 episodeName: str = None,
                 firstAired: str = None,
                 id: str = None,
                 lastUpdated: str = None,
                 overview: str = None):
        self.overview = overview
        self.lastUpdated = lastUpdated
        self.id = id
        self.firstAired = firstAired
        self.episodeName = episodeName
        self.dvdSeason = dvdSeason
        self.dvdEpisodeNumber = dvdEpisodeNumber
        self.airedSeason = airedSeason
        self.airedEpisodeNumber = airedEpisodeNumber
        self.absoluteNumber = absoluteNumber
