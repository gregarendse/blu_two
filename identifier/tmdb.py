from typing import List

import requests


class Page(object):
    def __init__(self, page: int = 0, total_results: int = 0, total_pages: int = 0):
        self.page: int = int(page)
        self.total_results: int = int(total_results)
        self.total_pages: int = int(total_pages)


class Result(object):
    def __init__(self, vote_count: int = None, id: int = None, video: bool = None,
                 vote_average: float = None, title: str = None, popularity: float = None, poster_path: str = None,
                 original_language: str = None, original_title: str = None, genre_ids=None, backdrop_path: str = None,
                 adult: bool = False, overview: str = None, release_date: str = None):
        if genre_ids is None:
            genre_ids = []
        self.genre_ids = genre_ids
        self.vote_count: int = int(vote_count)
        self.id: int = int(id)
        self.video: bool = bool(video)
        self.vote_average: float = float(vote_average)
        self.title: str = str(title)
        self.popularity: float = float(popularity)
        self.poster_path: str = str(poster_path)
        self.original_language: str = str(original_language)
        self.original_title: str = str(original_title)
        self.backdrop_path: str = str(backdrop_path)
        self.adult: bool = bool(adult)
        self.overview: str = str(overview)
        self.release_date: str = str(release_date)

    def get_year(self) -> int:
        if self.release_date is not None:
            return int(self.release_date.split('-')[0])


class SearchResponse(object):
    def __init__(self, page: Page = Page(), results: List[Result] = None):
        if results is None:
            results = []
        self.page: Page = page
        self.results: List[Result] = results


class TMDb(object):
    """

    """
    url = "https://api.themoviedb.org/3/search/movie"

    def movie_search(self, query: str, language: str = 'en-US', include_adult: bool = False, region: str = None,
                     year: int = None, primary_release_year: int = None) -> SearchResponse:
        querystring = {
            "api_key": self.api_key,
            "language": language,
            "query": query,
            "include_adult": include_adult,
            "region": region,
            "year": year,
            "primary_release_year": primary_release_year
        }
        headers = {
            'Cache-Control': "no-cache"
        }

        response = requests.get(url=self.url, headers=headers, params=querystring)

        if 200 <= response.status_code <= 299:
            results: List[Result] = []
            for result in response.json()['results']:
                results.append(Result(
                    vote_count=result['vote_count'],
                    id=result['id'],
                    video=result['video'],
                    vote_average=result['vote_average'],
                    title=result['title'],
                    popularity=result['popularity'],
                    poster_path=result['poster_path'],
                    original_language=result['original_language'],
                    original_title=result['original_title'],
                    genre_ids=result['genre_ids'],
                    backdrop_path=result['backdrop_path'],
                    adult=result['adult'],
                    overview=result['overview'],
                    release_date=result['release_date']
                ))
            return SearchResponse(
                page=Page(
                    page=response.json()['page'],
                    total_pages=response.json()['total_pages'],
                    total_results=response.json()['total_results']
                ),
                results=results
            )
        else:
            print(response.text)
            raise Exception(response.status_code)
