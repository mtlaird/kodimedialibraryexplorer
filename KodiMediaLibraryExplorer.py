from KodiMysqlClient import KodiMysqlClient
from flask import Flask, render_template
app = Flask(__name__)


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

    return render_template("movie_detail.html", movie=db_movie, actors=db_actors)


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


@app.route("/movies/director/<director_name>")
def movies_by_director(director_name):
    client = KodiMysqlClient()
    db_movies = client.get_movies_by_director(director_name)

    return render_template("movies.html", movies=db_movies)


@app.route("/movies/writer/<writer_name>")
def movies_by_writer(writer_name):
    client = KodiMysqlClient()
    db_movies = client.get_movies_by_writer(writer_name)

    return render_template("movies.html", movies=db_movies)


@app.route("/movies/actor/<actor_id>")
def movies_by_actor(actor_id):
    client = KodiMysqlClient()
    db_movies = client.get_movies_by_actor(actor_id=actor_id)

    return render_template("movies.html", movies=db_movies)


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
