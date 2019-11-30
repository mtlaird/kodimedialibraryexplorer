import csv
import json


class Taglist:
    def __init__(self, list_name):
        with open('taglists_meta/' + list_name + '.json') as f:
            self.metadata = json.load(f)

        self.movies = []
        with open('taglists_data/' + self.metadata['source']) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.movies.append(row)

    def movies_tuple(self):

        return tuple(movie['title'] for movie in self.movies)
