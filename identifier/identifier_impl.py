import re
from typing import Dict

from blu import Config
from identifier import TVDB
from identifier.model.series_search_data import SeriesSearchData
from identifier.model.title import Episode
from makeMKV.model.disc import Disc
from makeMKV.model.title import Title


class Identifier(object):
    config: Config = Config()

    def __init__(self):
        self.tvdb = TVDB(apikey=self.config.cfg['identifier']['theTVDB']['api_key'],
                         userkey=self.config.cfg['identifier']['theTVDB']['user_key'],
                         username=self.config.cfg['identifier']['theTVDB']['username'])

    def identify(self, disc: Disc) -> Disc:
        title: str = self.__get_nice_title__(disc.name)

        if self.__is_series__(disc.name):
            disc_number: int = self._get_disc_number(disc.name)
            season: int = self._get_season_number(disc.name)

            series: SeriesSearchData = self.tvdb.search(title)[0]
            tvdb_episodes = self.tvdb.getEpisode(series.id, season)
            episodes: Dict[int, Episode] = {}
            for episode in tvdb_episodes:
                episodes[episode.airedEpisodeNumber] = (Episode(
                    overview=episode.overview,
                    id=episode.id,
                    name=episode.episodeName,
                    season=episode.airedSeason,
                    episode=episode.airedEpisodeNumber,
                    number=episode.absoluteNumber
                ))

            # Assuming only 2 discs per season for now...
            factor = (len(disc.titles) / len(tvdb_episodes))
            start: int = round((disc_number - 1) * factor * len(tvdb_episodes))
            end: int = round((disc_number) * factor * len(tvdb_episodes))

            if disc_number == 1:
                start = 0
            elif disc_number == 2:
                start = len(tvdb_episodes) - len(disc.titles) - 1

            end = start + len(disc.titles)

            for i in range(start, end):
                title: Title = disc.ordered_titles[i - start]
                episode: Episode = episodes.get(i + 1)

                title.name = episode.name
                title.episode = episode.episode
                title.season = episode.season
                title.series = series.seriesName

            return disc

    def __get_nice_title__(self, disc_title) -> str:
        regex = re.compile(r'(DISC[_ ]?(\d+))|(D[_ ]?(\d+))|(SEASON[_ ]?(\d+))|(S[_ ]?(\d+))', re.IGNORECASE)
        working = regex.sub("", disc_title)  # Remove Season and disc
        working = re.sub(r'_', ' ', working)  # Replace '_' with spaces
        return working.strip()  # Remove trailing/leading spaces

    def __is_series__(self, disc_title) -> bool:
        search = re.compile(r'(DISC[_ ]?(\d+))|(D[_ ]?(\d+))|(SEASON[_ ]?(\d+))|(S[_ ]?(\d+))', re.IGNORECASE)
        if search.search(disc_title):
            return True
        else:
            return False

    def _get_disc_number(self, disc_title) -> int:
        search = re.compile(r'(DISC[_ ]?(\d+))|(D[_ ]?(\d+))', re.IGNORECASE)
        s = search.search(disc_title)

        counter = 0
        while s.group(len(s.groups()) - counter) is None:
            counter = counter + 1

        return int(s.group(len(s.groups()) - counter))

    def _get_season_number(self, disc_title) -> int:
        search = re.compile(r'(SEASON[_ ]?(\d+))|(S[_ ]?(\d+))', re.IGNORECASE)
        s = search.search(disc_title)

        counter = 0
        while s.group(len(s.groups()) - counter) is None:
            counter = counter + 1

        return int(s.group(len(s.groups()) - counter))
