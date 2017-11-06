import fire

from identifier.tvdb import TVDB


class CLI(object):
    def __init__(self):
        self.tvdb = TVDB(
            apikey='CCE5812818679F39', userkey='D1129E2353CFFE29', username='coolman565'
        )

    def search(self, name):
        print(self.tvdb.search(name))

    def getEpisode(self, seriesId: int, episode: int):
        print(self.tvdb.getEpisode(seriesId, episode))


if __name__ == '__main__':
    fire.Fire(CLI)
