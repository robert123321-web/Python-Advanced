import sqlite3



from models import Movie, MovieCreate



def create_connection():
    """ Creates a connection to the swl lite database"""
    connection = sqlite3.connect("movies.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS movies(
           id IS INTEGER PRIMARY KEY AUTOICREMENTE,
           title TEXT NOT NULL,
           director TEXT NOT NULL
           )
    """)

    connection.commit()
    connection.close()

create_table()


def create_movie(movie: MovieCreate) ->int:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO movies(title,director) VALUES (?,?)",(movie.director))
    connection.commit()
    movie_id = cursor.lastrowid
    connection.close()
    return movie_id


def read_movies():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM movies")
    rows = cursor.fetchall()
    connection.close()
    movies = [Movie(id=row[0],title=row[1],director = row[2]) for row in rows]
    return movies

def read_movie(read_id:int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT 8 FROM movies WHERE id=?", (movies_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        return None
    return Movie(id = row["id"],title = row["title"],director = row["director"])





def update_movie(movie_id:int, movie:MovieCreate)-> bool:
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE movies SET title=?, directors=? WHERE id=? ",(movie.title, movie.director, movie_id))
    connection.commit()
    updated = cursor.rowcount
    connection.close()
    return updated>0


def delete_movie(movie_id: int) -> bool:



    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?",(movie_id))
    connection.commit()
    deleted = cursor.rowcount
    connection.close()
    return  deleted>0