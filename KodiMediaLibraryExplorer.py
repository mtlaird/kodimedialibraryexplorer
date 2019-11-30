from flask import Flask, render_template, request

import TMDBApi
import logging
from KodiMysqlClient import KodiMysqlClient
from KodiTaglist import Taglist

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/movies")
def movies():
    client = KodiMysqlClient()
    db_movies = client.get_all_movie_titles()

    return render_template("movies.html", movies=db_movies)


@app.route("/movies/id/<movie_id>")
def movie_detail(movie_id):
    client = KodiMysqlClient()
    db_movie = client.get_movie_info(movie_id=movie_id)
    db_actors = client.get_actors_by_movie(movie_id=movie_id)
    db_tags = client.get_movie_tags(movie_id=movie_id)

    return render_template("movie_detail.html", movie=db_movie, actors=db_actors, tags=db_tags)


@app.route("/tvshows")
def tvshows():
    client = KodiMysqlClient()
    db_tvshows = client.get_all_tvshow_titles()

    return render_template("tvshows.html", tvshows=db_tvshows)


@app.route("/tvshows/id/<tvshow_id>")
def tvshow_detail(tvshow_id):
    client = KodiMysqlClient()
    db_show = client.get_tvshow_info(show_id=tvshow_id)
    db_episodes = client.get_episode_count_per_season_by_tvshow(show_id=tvshow_id)

    return render_template("tvshow_detail.html", tvshow=db_show, episodes=db_episodes)


@app.route("/actors")
def actors():
    client = KodiMysqlClient()
    db_actors = client.get_all_actors()

    return render_template("actors.html", actors=db_actors)


@app.route("/directors")
def directors():
    client = KodiMysqlClient()
    db_directors = client.get_all_movie_directors()

    return render_template("directors.html", directors=db_directors)


@app.route("/person/<person_name>")
def person_detail(person_name):
    client = KodiMysqlClient()
    db_movies_dir = client.get_movies_by_director(person_name)
    db_movies_dir_dict = client.convert_db_movie_list_to_dict(db_movies_dir)
    db_movies_wri = client.get_movies_by_writer(person_name)
    db_movies_wri_dict = client.convert_db_movie_list_to_dict(db_movies_wri)
    db_movies_act = client.get_movies_by_actor(actor_name=person_name)
    db_movies_act_dict = client.convert_db_movie_list_to_dict(db_movies_act)

    try:
        tmdb_person = TMDBApi.Person(name=person_name)
    except TMDBApi.TMDBSearchException:
        return render_template("person.html", db_movies_act=db_movies_act, db_movies_wri=db_movies_wri,
                               db_movies_dir=db_movies_dir)

    return render_template("person.html", db_movies_act_dict=db_movies_act_dict, db_movies_wri_dict=db_movies_wri_dict,
                           db_movies_dir_dict=db_movies_dir_dict, tmdb_movies_act=tmdb_person.get_movies_as_actor(),
                           tmdb_movies_wri=tmdb_person.get_movies_as_writer(), info=tmdb_person.info,
                           tmdb_movies_dir=tmdb_person.get_movies_as_director())


@app.route("/movies/genre/<genre_name>")
def movies_by_genre(genre_name):
    client = KodiMysqlClient()
    db_movies = client.get_movies_by_genre(genre_name)

    return render_template("movies.html", movies=db_movies)


@app.route("/tvshows/genre/<genre_name>")
def tvshows_by_genre(genre_name):
    client = KodiMysqlClient()
    db_tvshows = client.get_tvshows_by_genre(genre_name)

    return render_template("tvshows.html", tvshows=db_tvshows)


@app.route("/tags")
def tags():
    client = KodiMysqlClient()
    db_tags = client.get_all_tags()

    return render_template("tags.html", tags=db_tags)


@app.route("/tags/<tag_id>")
def movies_by_tag(tag_id):
    client = KodiMysqlClient()
    db_movies = client.get_movie_titles_by_tag(tag_id)

    return render_template("tag_detail.html", movies=db_movies)


@app.route("/taglists/<list_name>", methods=["GET", "POST"])
def taglist_by_name(list_name):
    tags_added = None
    client = KodiMysqlClient()
    taglist = Taglist(list_name)

    db_tag_movies_dict, db_tag = client.get_movies_dict_by_tag_name(taglist.metadata['name'])
    db_movies = client.get_movies_from_title_list(taglist.movies_tuple())
    db_movies_dict = client.convert_db_movie_list_to_dict(db_movies)

    if request.method == "POST" and request.form['add_tags'] == 'true':
        db_movies_no_tag_dict = client.get_dict_difference(db_movies_dict, db_tag_movies_dict)
        tags_added = client.add_tag_to_movie_dict(db_tag, db_movies_no_tag_dict)
        db_tag_movies_dict, db_tag = client.get_movies_dict_by_tag_name(taglist.metadata['name'])

    return render_template("tag_list_detail.html", taglist=taglist.metadata, taglist_movies=taglist.movies,
                           db_tag=db_tag, db_movies_dict=db_movies_dict, db_tag_movies_dict=db_tag_movies_dict,
                           tags_added=tags_added)
