import mysql.connector
from flask import current_app


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
            self.kodi_mysql_address = current_app.config["mysqlserver-host"]
        except KeyError:
            self.kodi_mysql_address = "127.0.0.1"
        try:
            self.kodi_mysql_video_db = current_app.config["mysql-video-db"]
        except KeyError:
            self.kodi_mysql_video_db = "MyVideos121"

        self.cnx = mysql.connector.connect(
            user="kodi",
            password="kodi",
            host=self.kodi_mysql_address,
            database=self.kodi_mysql_video_db
        )

    @staticmethod
    def convert_db_movie_list_to_dict(movie_list):

        ret_dict = {}

        for list_item in movie_list:
            ret_dict[list_item['title']] = list_item['id']

        return ret_dict

    @staticmethod
    def get_dict_difference(list1, list2):
        ret_dict = {}
        for key in list1:
            if key not in list2:
                ret_dict[key] = list1[key]
        return ret_dict

    @staticmethod
    def get_movie_list_difference(list1, list2):
        ret_list = []
        for item in list1:
            if item not in list2:
                ret_list.append(item)
        return ret_list

    def get_all_movie_titles(self):

        cursor = self.cnx.cursor()

        query = "select idMovie, c00 from movie order by c00"
        cursor.execute(query)

        ret = []
        for (idMovie, c00) in cursor:
            ret.append({"id": idMovie, "title": c00})

        return ret

    def get_movies_for_csv(self):

        cursor = self.cnx.cursor()

        query = "select c00 as title, premiered from movie order by title"
        cursor.execute(query)

        ret = []
        for (title, premiered) in cursor:
            ret.append((title, premiered))

        return ret

    def get_movie_titles_by_search(self, search):

        cursor = self.cnx.cursor()

        query = "select idMovie, c00 from movie where c00 like %s order by c00"
        cursor.execute(query, ('%' + search + '%',))

        ret = []
        for (idMovie, c00) in cursor:
            ret.append({"id": idMovie, "title": c00})

        return ret

    def get_movie_info(self, movie_title=None, movie_id=None):

        cursor = self.cnx.cursor()
        query = "select idMovie, c00, c06, c14, c15, c18, c21, premiered, idSet from movie "
        if movie_title:
            query += "where c00 = %s"
            cursor.execute(query, (movie_title,))
        elif movie_id:
            query += "where idMovie = %s"
            cursor.execute(query, (movie_id,))
        else:
            return {}

        for (idMovie, c00, c06, c14, c15, c18, c21, premiered, idSet) in cursor:
            return {
                "id": idMovie, "title": c00, "writer": check_for_split(c06),
                "genre": check_for_split(c14), "director": check_for_split(c15),
                "production company": c18, "country": c21, "premiered": premiered,
                "set_id": idSet
            }

    def get_movie_by_title_and_year(self, title, year):

        cursor = self.cnx.cursor()
        query = "select idMovie, c00, premiered from movie where c00 = %s and premiered like %s"
        cursor.execute(query, (title, '%' + year + '%'))

        for (idMovie, c00, premiered) in cursor:
            return {"id": idMovie, "title": c00, "premiered": premiered}

        return {}

    def get_movie_tags(self, movie_id):

        cursor = self.cnx.cursor()
        query = "select tl.tag_id, name from tag_link tl inner join tag on tl.tag_id = tag.tag_id " \
                "where media_id = %s and media_type = 'movie'"
        cursor.execute(query, (movie_id,))

        ret = []
        for (tag_id, name) in cursor:
            ret.append({"tag_id": tag_id, "tag_name": name})

        return ret

    def get_movie_title_and_release_by_tag(self, tag_id):

        cursor = self.cnx.cursor()
        query = "select idMovie, c00, premiered from tag_link tl inner join movie on tl.media_id = movie.idMovie " \
                "where tag_id = %s"
        cursor.execute(query, (tag_id,))

        ret = []
        for (idMovie, c00, premiered) in cursor:
            ret.append({"id": idMovie, "title": c00, "premiered": premiered})

        return ret

    def get_movies_dict_by_tag_name(self, tag_name):
        tag = self.get_tag_by_name(tag_name)

        if tag:
            tag_movies = self.get_movie_title_and_release_by_tag(tag['tag_id'])
            return self.convert_db_movie_list_to_dict(tag_movies), tag
        else:
            return {}, tag

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

    def get_movies_from_title_list(self, title_list):
        cursor = self.cnx.cursor()

        format_strings = ','.join(['%s'] * len(title_list))
        query = "select idMovie, c00, premiered from movie where c00 IN (%s)" % format_strings
        cursor.execute(query, title_list)
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

    def get_tvshows_for_csv(self):

        cursor = self.cnx.cursor()

        query = "select s.c00 as title, s.c05 as start_date, count(idEpisode) as episodes, " \
                "count(distinct (idSeason)) as seasons from tvshow s " \
                "inner join episode e on s.idShow = e.idShow group by s.idShow order by title"
        cursor.execute(query)

        ret = []
        for (title, start_date, episodes, seasons) in cursor:
            ret.append((title, start_date, episodes, seasons))

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

    def get_season_id(self, show_id, season):

        cursor = self.cnx.cursor()

        query = "select idSeason from seasons " \
                "where idShow = %s and season = %s"

        cursor.execute(query, (show_id, season))

        for (idSeason,) in cursor:
            return idSeason

    def get_episode_titles_by_tvshow_and_season(self, season_id, show_id):

        cursor = self.cnx.cursor()

        query = "select CAST(e.c13 as UNSIGNED) as number, e.c05 as airdate, e.c00 as title from seasons s " \
                "inner join tvshow t on s.idShow = t.idShow " \
                "inner join episode e on s.idSeason = e.idSeason " \
                "where s.idSeason = %s " \
                "and t.idShow = %s " \
                "order by number"
        cursor.execute(query, (season_id, show_id))

        ret = []
        for (number, airdate, title) in cursor:
            ret.append({"number": number, "airdate": airdate, "title": title})

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

    def create_tag(self, tag_name):

        cursor = self.cnx.cursor()

        query = "insert into tag (name) values (%s)"
        cursor.execute(query, (tag_name,))

        self.cnx.commit()

    def get_all_tags(self):

        cursor = self.cnx.cursor()

        query = "select tag_id, name from tag"
        cursor.execute(query)
        ret = []
        for (tag_id, name) in cursor:
            ret.append({"tag_id": tag_id, "tag_name": name})

        return ret

    def get_tag_by_name(self, tagname):

        cursor = self.cnx.cursor()

        query = "select tag_id, name from tag where name = %s"
        cursor.execute(query, (tagname,))

        for (tag_id, name) in cursor:
            return {"tag_id": tag_id, "tag_name": name}

        return {}

    def add_tag_to_movie(self, tag_id, movie_id, commit=True):

        cursor = self.cnx.cursor()

        query = "insert into tag_link (tag_id, media_id, media_type) values (%s, %s, %s)"
        cursor.execute(query, (tag_id, movie_id, 'movie'))

        if commit:
            self.cnx.commit()

    def add_tag_to_movie_dict(self, tag, movie_dict):
        tags_added = 0
        for movie in movie_dict:
            self.add_tag_to_movie(tag['tag_id'], movie_dict[movie], False)
            tags_added += 1

        self.cnx.commit()

        return tags_added

    def add_tag_to_movies_check_year(self, tag, db_movies, source_movies):
        pass_ok = []
        for movie in db_movies:
            for s_movie in source_movies:
                if movie['title'] == s_movie['title']:
                    if s_movie['year'] in movie['premiered']:
                        pass_ok.append(movie)

        tags_added = self.add_tag_to_movie_dict(tag, self.convert_db_movie_list_to_dict(pass_ok))

        return tags_added

    def get_all_sets(self):

        cursor = self.cnx.cursor()

        query = "select idSet, strSet from sets order by strSet"
        cursor.execute(query)
        ret = []
        for (idSet, strSet) in cursor:
            ret.append({"set_id": idSet, "set_name": strSet})

        return ret

    def get_set_details_by_id(self, set_id):

        cursor = self.cnx.cursor()

        query = "select idSet, strSet, strOverview from sets where idSet = %s"
        cursor.execute(query, (set_id,))

        for (idSet, strSet, strOverview) in cursor:
            return {"set_id": idSet, "set_name": strSet, "set_overview": strOverview}

        return {}

    def get_movies_by_set(self, set_id):

        cursor = self.cnx.cursor()

        query = "select idMovie, c00 from movie where idSet = %s"
        cursor.execute(query, (set_id,))

        ret = []
        for (idMovie, c00) in cursor:
            ret.append({"id": idMovie, "title": c00})

        return ret

    def get_all_movie_poster_art_urls(self):

        cursor = self.cnx.cursor()

        query = "select art_id, media_id, c00 as movie_title, media_type, art_type, url from art " \
                "inner join movie on art.media_id = movie.idMovie " \
                "where media_type = 'movie' and type = 'poster'"
        cursor.execute(query)

        ret = []
        for (art_id, media_id, movie_title, media_type, art_type, url) in cursor:
            ret.append({"art_id": art_id, "media_id": media_type, "type": art_type, "url": url,
                        "movie_title": movie_title})

        return ret

    def get_movie_poster_art_by_id(self, movie_id):

        cursor = self.cnx.cursor()

        query = "select art_id, url from art " \
                "where media_type = 'movie' and type = 'poster' and media_id = %s "

        cursor.execute(query, (movie_id,))

        for (art_id, url) in cursor:
            return {"art_id": art_id, "url": url}

        return {}

    def update_movie_poster_art_url(self, art_id, new_url, commit=True):

        cursor = self.cnx.cursor()
        query = "update art set url = %s where art_id = %s"

        cursor.execute(query, (new_url, art_id))

        if commit:
            self.cnx.commit()
