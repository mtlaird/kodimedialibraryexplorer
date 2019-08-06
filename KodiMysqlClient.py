import mysql.connector
import json


def strip_array_elements(a):
    new_a = []
    for e in a:
        new_a.append(e.strip())
    return new_a


def check_for_split(s):
    if '/' in s:
        return strip_array_elements(s.split('/'))
    else:
        return s


class KodiMysqlClient:

    def __init__(self):
        try:
            with open("config.json") as f:
                config = json.load(f)
                mysqlserver_host = config["mysqlserver-host"]
        except IOError:
            mysqlserver_host = "127.0.0.1"
        self.kodi_mysql_address = mysqlserver_host
        self.kodi_mysql_video_db = "MyVideos116"

        self.cnx = mysql.connector.connect(
            user="kodi",
            password="kodi",
            host=self.kodi_mysql_address,
            database=self.kodi_mysql_video_db
        )

    def get_all_movie_titles(self):

        cursor = self.cnx.cursor()

        query = "select idMovie, c00 from movie order by c00"
        cursor.execute(query)

        ret = []
        for (idMovie, c00) in cursor:
            ret.append({"id": idMovie, "title": c00})

        return ret

    def get_movie_info(self, movie_title=None, movie_id=None):

        cursor = self.cnx.cursor()
        query = "select idMovie, c00, c06, c14, c15, c18, c21, premiered from movie "
        if movie_title:
            query += "where c00 = %s"
            cursor.execute(query, (movie_title,))
        elif movie_id:
            query += "where idMovie = %s"
            cursor.execute(query, (movie_id,))
        else:
            return {}

        for (idMovie, c00, c06, c14, c15, c18, c21, premiered) in cursor:
            return {
                "id": idMovie, "title": c00, "writer": check_for_split(c06),
                "genre": check_for_split(c14), "director": check_for_split(c15),
                "production company": c18, "country": c21, "premiered": premiered
            }

    def get_all_movie_directors(self):

        cursor = self.cnx.cursor()

        query = "select c15, count(*) as count from movie group by c15 order by c15"
        cursor.execute(query)

        ret = []
        for (c15, count) in cursor:
            ret.append({"director": check_for_split(c15), "movie_count": count})

        return ret

    def get_movies_by_director(self, director_name):

        cursor = self.cnx.cursor()

        query = "select idMovie, c00, premiered from movie where c15 like %s order by c00"
        cursor.execute(query, ("%" + director_name + "%",))

        ret = []
        for (idMovie, c00, premiered) in cursor:
            ret.append({"id": idMovie, "title": c00, "premiered": premiered})

        return ret

    def get_movies_by_writer(self, writer_name):
        cursor = self.cnx.cursor()

        query = "select idMovie, c00, premiered from movie where c06 like %s order by c00"
        cursor.execute(query, ("%" + writer_name + "%",))

        ret = []
        for (idMovie, c00, premiered) in cursor:
            ret.append({"id": idMovie, "title": c00, "premiered": premiered})

        return ret

    def get_movies_by_genre(self, genre):
        cursor = self.cnx.cursor()

        query = "select idMovie, c00, premiered from movie where c14 like %s order by c00"
        cursor.execute(query, ("%" + genre + "%",))
        ret = []
        for (idMovie, c00, premiered) in cursor:
            ret.append({"id": idMovie, "title": c00, "premiered": premiered})

        return ret

    def get_all_actors(self):

        cursor = self.cnx.cursor()

        query = "select actor_id, name from actor order by name"
        cursor.execute(query)

        ret = []
        for (actor_id, name) in cursor:
            ret.append({"id": actor_id, "name": name})

        return ret

    def get_actors_by_movie(self, movie_title=None, movie_id=None):

        cursor = self.cnx.cursor()

        query = "select a.actor_id, a.name from movie m " \
                "inner join actor_link al on m.idMovie = al.media_id " \
                "inner join actor a on al.actor_id = a.actor_id "
        if movie_title:
            query += "where m.c00 = %s and al.media_type = %s order by cast_order"
            cursor.execute(query, (movie_title, "movie"))
        elif movie_id:
            query += "where m.idMovie = %s and al.media_type = %s order by cast_order"
            cursor.execute(query, (movie_id, "movie"))
        else:
            return []

        ret = []
        for (actor_id, name) in cursor:
            ret.append({"name": name, "id": actor_id})
        return ret

    def get_movies_by_actor(self, actor_name=None, actor_id=None):

        cursor = self.cnx.cursor()

        query = "select m.idMovie, m.c00 from movie m " \
                "inner join actor_link al on m.idMovie = al.media_id " \
                "inner join actor a on al.actor_id = a.actor_id "
        if actor_name:
            query += "where a.name = %s and al.media_type = %s order by m.c00"
            cursor.execute(query, (actor_name, "movie"))
        elif actor_id:
            query += "where a.actor_id = %s and al.media_type = %s order by m.c00"
            cursor.execute(query, (actor_id, "movie"))
        else:
            return []

        ret = []
        for (idMovie, c00) in cursor:
            ret.append({"id": idMovie, "title": c00})
        return ret

    def get_all_tvshow_titles(self):

        cursor = self.cnx.cursor()

        query = "select idShow, c00 from tvshow order by c00"
        cursor.execute(query)

        ret = []
        for (idShow, c00) in cursor:
            ret.append({"id": idShow, "title": c00})

        return ret

    def get_tvshow_info(self, show_name=None, show_id=None):

        cursor = self.cnx.cursor()

        query = "select idShow, c00, c05, c08, c13, c14 from tvshow t "

        if show_name:
            query += "where t.c00 = %s"
            cursor.execute(query, (show_name,))
        elif show_id:
            query += "where t.idShow = %s"
            cursor.execute(query, (show_id,))
        else:
            return []

        for (idShow, c00, c05, c08, c13, c14) in cursor:
            return {
                "id": idShow, "title": c00, "first_aired": c05,
                "genre": check_for_split(c08), "rated": c13, "studio": c14
            }

    def get_episode_titles_by_tvshow(self, show_name=None, show_id=None):

        cursor = self.cnx.cursor()

        query = "select s.name, e.c00 from seasons s " \
                "inner join tvshow t on s.idShow = t.idShow " \
                "inner join episode e on s.idSeason = e.idSeason "
        if show_name:
            query += "where t.c00 = %s"
            cursor.execute(query, (show_name,))
        elif show_id:
            query += "where t.idShow = %s"
            cursor.execute(query, (show_id,))
        else:
            return []

        ret = []
        for (name, c00) in cursor:
            ret.append({"season": name, "title": c00})

        return ret

    def get_episode_count_per_season_by_tvshow(self, show_name=None, show_id=None):

        cursor = self.cnx.cursor()

        query = "select s.season, count(*) as count from seasons s " \
                "inner join tvshow t on s.idShow = t.idShow " \
                "inner join episode e on s.idSeason = e.idSeason "
        if show_name:
            query += "where t.c00 = %s group by s.season"
            cursor.execute(query, (show_name,))
        elif show_id:
            query += "where t.idShow = %s group by s.season"
            cursor.execute(query, (show_id,))
        else:
            return []

        ret = []
        for (season, count) in cursor:
            ret.append({"season": season, "episode_count": count})

        return ret

    def get_tvshow_titles_by_actor(self, actor_name=None, actor_id=None):

        cursor = self.cnx.cursor()

        query = "select idShow, t.c00 from tvshow t " \
                "inner join actor_link al on t.idShow = al.media_id " \
                "inner join actor a on al.actor_id = a.actor_id "
        if actor_name:
            query += "where a.name = %s and al.media_type = %s order by t.c00"
            cursor.execute(query, (actor_name, "tvshow"))
        elif actor_id:
            query += "where a.actor_id = %s and al.media_type = %s order by t.c00"
            cursor.execute(query, (actor_id, "tvshow"))
        else:
            return []

        ret = []
        for (idShow, c00) in cursor:
            ret.append({"id": idShow, "title": c00})

        return ret

    def get_tvshows_by_genre(self, genre):

        cursor = self.cnx.cursor()

        query = "select idShow, c00 from tvshow where c08 like %s order by c00"
        cursor.execute(query, ("%" + genre + "%",))
        ret = []
        for (idShow, c00) in cursor:
            ret.append({"id": idShow, "title": c00})

        return ret
