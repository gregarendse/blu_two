import json
from typing import List

import requests

from identifier.model.auth import Auth
from identifier.model.basic_episode import BasicEpisode
from identifier.model.series_search_data import SeriesSearchData
from identifier.model.token import Token


class TVDB(object):
    host: str = 'https://api.thetvdb.com'

    def __init__(self, apikey: str, userkey: str, username: str):
        self.auth = Auth(apikey, userkey, username)
        self.jsonDecoder = json.JSONDecoder()
        self.token = self.login()

    def login(self) -> Token:
        payload = json.dumps({
            'apikey': self.auth.apikey,
            'userkey': self.auth.userkey,
            'username': self.auth.username
        })
        # payload = "{\"apikey\":\"{apikey}\",\"userkey\":\"{userkey}\",\"username\":\"{username}\"}" \
        #     .format(apikey=self.auth.apikey, userkey=self.auth.userkey, username=self.auth.username)
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.post("{}/login".format(self.host), data=payload, headers=headers)

        if response.ok is not True:
            raise Exception(response.status_code)

        return Token(self.jsonDecoder.decode(response.text)['token'])

    def search(self, name: str) -> List[SeriesSearchData]:
        querystring = {"name": name}

        headers = {
            'accept-language': "en",
            'authorization': "Bearer {}".format(self.token.token),
            'cache-control': "no-cache",
        }

        response = requests.get("{}/search/series".format(self.host), headers=headers, params=querystring)

        if response.ok is not True:
            raise Exception(response.status_code)

        json_response = json.loads(response.text)['data']
        seriesSearchData = []

        for item in json_response:
            seriesSearchData.append(SeriesSearchData(
                item['aliases'],
                item['banner'],
                item['firstAired'],
                item['id'],
                item['network'],
                item['overview'],
                item['seriesName'],
                item['status']
            ))

        return seriesSearchData

    def getEpisode(self, seriesId: int, episode: int) -> List[BasicEpisode]:
        querystring = {"airedSeason": str(episode)}

        headers = {
            'accept-language': "en",
            'authorization': "Bearer {}".format(self.token.token),
            'cache-control': "no-cache",
            'postman-token': "068c458a-4715-2934-bd03-8a5aaa265adf"
        }

        response = requests.get("{host}/series/{seriesId}/episodes/query".format(host=self.host, seriesId=seriesId),
                                headers=headers,
                                params=querystring)

        if response.ok is not True:
            raise Exception(response.status_code)

        json_response = json.loads(response.text)['data']
        episodes = []

        for item in json_response:
            episodes.append(BasicEpisode(
                item['absoluteNumber'],
                item['airedEpisodeNumber'],
                item['airedSeason'],
                item['dvdEpisodeNumber'],
                item['dvdSeason'],
                item['episodeName'],
                item['firstAired'],
                item['id'],
                item['lastUpdated'],
                item['overview']
            ))

        return episodes
