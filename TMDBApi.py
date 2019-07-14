import tmdbsimple as tmdb
import json

with open('config.json') as f:
    config = json.load(f)
    tmdb.API_KEY = config['tmdb-api-key']


def get_titles_from_movie_list(movie_list):
    ret_list = []
    for movie in movie_list:
        if movie['title'] not in ret_list:
            ret_list.append(movie['title'])
    return ret_list


class TMDBSearchException(Exception):
    pass


class Person:

    def __init__(self, tmdb_id=None, name=None):
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

        return [movie for movie in self.movies['crew'] if (movie['department'] == role_type or movie['job'] == role_type)]

    def get_movies_as_writer(self):

        return self.get_movies_by_crew_role('Writing')

    def get_movies_as_director(self):

        return self.get_movies_by_crew_role('Directing')

    def get_movies_as_actor(self):

        return self.movies['cast']

    def get_tv_shows_as_actor(self):

        return self.tv_shows['cast']
