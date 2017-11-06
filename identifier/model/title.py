class Title(object):
    def __init__(self, overview: str = None, id: str = None, name: str = None):
        self.overview: str = overview
        self.id: str = id
        self.name: str = name


class Episode(Title):
    def __init__(self,
                 overview: str = None,
                 id: str = None,
                 name: str = None,
                 season: int = None,
                 episode: int = None,
                 number: int = None):
        super().__init__(overview, id, name)
        self.season: int = season
        self.episode: int = episode
        self.number: int = number
