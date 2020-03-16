import csv
import json
from os import listdir
from flask import current_app


class Taglist:
    def __init__(self, list_name):
        taglist_root = current_app.config["root-path"]
        if taglist_root != '' and taglist_root[-1] != '/':
            taglist_root += '/'
        if list_name.endswith(".json"):
            with open(taglist_root + 'taglists_meta/' + list_name) as f:
                self.metadata = json.load(f)
                self.name = list_name.split(".json")[0]
        else:
            with open(taglist_root + 'taglists_meta/' + list_name + '.json') as f:
                self.metadata = json.load(f)
                self.name = list_name

        self.movies = []
        with open(taglist_root + 'taglists_data/' + self.metadata['source']) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.movies.append(row)

    def movies_tuple(self):

        return tuple(movie['title'] for movie in self.movies)


class TaglistDirectory:
    def __init__(self):
        taglist_root = current_app.config["root-path"]
        if taglist_root != '' and taglist_root[-1] != '/':
            taglist_root += '/'
        self.taglists = {}
        for f in listdir(taglist_root + "taglists_meta"):
            temp = Taglist(f)
            self.taglists[temp.metadata['name']] = temp
