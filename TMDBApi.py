import tmdbsimple as tmdb
from flask import current_app
from requests import head


def get_titles_from_movie_list(movie_list):
    ret_list = []
    for movie in movie_list:
        if movie['title'] not in ret_list:
            ret_list.append(movie['title'])
    return ret_list


def check_url_status_code(url):
    response = head(url)
    return response.status_code


class TMDBSearchException(Exception):
    pass


class Person:

    def __init__(self, tmdb_id=None, name=None):
        tmdb.API_KEY = current_app.config["tmdb-api-key"]
        self.tmdb_id = None
        if tmdb_id:
            self.tmbd_id = tmdb_id
        elif name:
            temp = tmdb.Search().person(query=name)
            result = temp['results'][0]
            self.tmdb_id = result['id']
        if not self.tmdb_id:
            print("TMDB search failed. Search type: 'person' Search string: '{}'".format(name))
            raise TMDBSearchException
        person = tmdb.People(self.tmdb_id)

        self.info = person.info()
        self.movies = person.movie_credits()
        self.tv_shows = person.tv_credits()
        self.external_ids = person.external_ids()

    def get_movies_by_crew_role(self, role_type):

        return [movie for movie in self.movies['crew'] if (movie['department'] == role_type or
                                                           movie['job'] == role_type)]

    def get_movies_as_writer(self):

        return self.get_movies_by_crew_role('Writing')

    def get_movies_as_director(self):

        return self.get_movies_by_crew_role('Directing')

    def get_movies_as_actor(self):

        return self.movies['cast']

    def get_tv_shows_as_actor(self):

        return self.tv_shows['cast']


class Collection:

    def __init__(self, tmdb_id=None, name=None):
        tmdb.API_KEY = current_app.config["tmdb-api-key"]
        self.tmdb_id = None
        if tmdb_id:
            self.tmdb_id = tmdb_id
        else:
            temp = tmdb.Search().collection(query=name)
            if len(temp['results']) == 0:
                print("TMDB search failed. Search type: 'collection' Search string: '{}'".format(name))
                raise TMDBSearchException
            result = temp['results'][0]
            self.tmdb_id = result['id']
        if not self.tmdb_id:
            print("TMDB search failed. Search type: 'collection' Search string: '{}'".format(name))
            raise TMDBSearchException

        coll = tmdb.Collections(self.tmdb_id)

        self.info = coll.info()
        self.name = self.info['name']
        self.overview = self.info['overview']
        self.parts = self.info['parts']

    def get_movies_in_collection(self):
        ret_list = []
        for p in self.parts:
            details = {'title': p['title'], 'popularity': p['popularity'],
                       'vote_average': p['vote_average'], 'overview': p['overview']}
            if 'release_date' in p:
                details['release_date'] = p['release_date']
            ret_list.append(details)

        return ret_list


class TVShow:

    def __init__(self, tmdb_id=None, name=None):
        tmdb.API_KEY = current_app.config["tmdb-api-key"]
        self.tmdb_id = None
        if tmdb_id:
            self.tmdb_id = tmdb_id
        else:
            temp = tmdb.Search().tv(query=name)
            if len(temp['results']) > 0:
                result = temp['results'][0]
                self.tmdb_id = result['id']
        if not self.tmdb_id:
            print("TMDB search failed. Search type: 'tv' Search string: '{}'".format(name))
            raise TMDBSearchException
        self.tv = tmdb.TV(self.tmdb_id)

        self.info = self.tv.info()

    def get_creator(self):
        return self.tv.created_by

    def get_first_air_date(self):
        return self.tv.first_air_date

    def get_last_air_date(self):
        return self.tv.last_air_date

    def get_number_of_episodes(self):
        return self.tv.number_of_episodes

    def get_number_of_seasons(self):
        return self.tv.number_of_seasons

    def get_overview(self):
        return self.tv.overview

    def get_seasons(self):
        return self.tv.seasons

    def get_status(self):
        return self.tv.status

    def get_show_info(self):
        return {"num_seasons": self.get_number_of_seasons(), "num_episodes": self.get_number_of_episodes(),
                "overview": self.get_overview(), "status": self.get_status(), "first_air": self.get_first_air_date(),
                "last_air": self.get_last_air_date()}


class Movie:

    def __init__(self, tmdb_id=None, name=None):
        tmdb.API_KEY = current_app.config["tmdb-api-key"]
        self.tmdb_id = None
        if tmdb_id:
            self.tmdb_id = tmdb_id
        else:
            temp = tmdb.Search().movie(query=name)
            if len(temp['results']) > 0:
                result = temp['results'][0]
                self.tmdb_id = result['id']
        if not self.tmdb_id:
            print("TMDB search failed. Search type: 'movie' Search string: '{}'".format(name))
            raise TMDBSearchException
        self.movie = tmdb.Movies(self.tmdb_id)

        self.info = self.movie.info()
        self.images = self.movie.images()

    def get_posters(self):

        return self.images['posters']
