import os
import platform
import time
from typing import Dict

import xmltodict

from blu import Config
from identifier import TVDB
from identifier.model.series_search_data import SeriesSearchData
from identifier.model.title import Episode
from identifier.tmdb import TMDb
from makeMKV.model.disc import Disc
from makeMKV.model.title import Title


class Identifier(object):
    config: Config = Config()

    def __init__(self):
        self.tvdb = TVDB(apikey=self.config.cfg['identifier']['theTVDB']['api_key'],
                         userkey=self.config.cfg['identifier']['theTVDB']['user_key'],
                         username=self.config.cfg['identifier']['theTVDB']['username'])
        self.tmdb = TMDb()

    def identify(self, disc: Disc) -> Disc:
        title: str = disc.get_nice_title()

        if disc.is_series():
            disc_number: int = disc.get_disc_number()
            season: int = disc.get_season_number()

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
        else:
            search_result = self.tmdb.movie_search(disc.name.replace('_', ' '))

            if search_result.page.total_results == 1:
                # disc.year = self.__get_year__('{location}/BDMV/META/DL/bdmt_eng.xml'.format(location=disc.location))
                disc.year = search_result.results[0].get_year()
                # disc.name = self.__get_name__('{location}/BDMV/META/DL/bdmt_eng.xml'.format(location=disc.location))
                disc.name = search_result.results[0].title

            return disc

    def __get_year__(self, path_to_file: str) -> int:
        """
        https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python

        Try to get the date that a file was created, falling back to when it was
        last modified if that isn't possible.
        See http://stackoverflow.com/a/39501288/1709587 for explanation.
        """
        seconds: int = 0
        if platform.system() == 'Windows':
            seconds = int(os.path.getctime(path_to_file))
        else:
            stat = os.stat(path_to_file)
            try:
                seconds = int(stat.st_birthtime)
            except AttributeError:
                # We're probably on Linux. No easy way to get creation dates here,
                # so we'll settle for when its content was last modified.
                seconds = int(stat.st_mtime)

        return int(time.strftime('%Y', time.localtime(seconds)))

    def __get_name__(self, path_to_file: str) -> str:
        with open(path_to_file, 'r') as file:
            content = file.read()

        try:
            xml = xmltodict.parse(content, encoding='UTF-8')
        except:
            xml = xmltodict.parse(content, encoding='ISO-8859-1')

        return xml['disclib']['di:discinfo']['di:title']['di:name']
