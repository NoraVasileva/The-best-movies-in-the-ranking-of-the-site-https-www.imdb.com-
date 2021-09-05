from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///Movies.db', echo=True) # създаване на базата банни
Base = declarative_base() # функция, чрез която създавам колони в базата от данни


class Movies(Base):
    """
    Creating a model for the database
    """
    __tablename__ = 'Movies'
    # описвам колоните от какъв тип да са:
    id = Column(Integer, primary_key=True)
    movie_name = Column(String(120), index=True)
    genre = Column(String(120), index=True)
    year = Column(String(4), index=True)
    rating = Column(String(10), index=True)
    url_images = Column(String(255))
    hours = Column(String(20), index=True)
    director = Column(String(120), index=True)
    actors = Column(String(255), index=True)
    link = Column(String(255), index=True)

    def __init__(self, movie_name=None, year=None, genre=None, rating=None, url_images=None, hours=None, director=None,
                 actors=None, link=None):
        """
        Entering attributes.
        :param movie_name: the name of the movie
        :param year: year of release
        :param genre: genre of the movie
        :param rating: rating of the movie
        :param url_images: link to the image of the movie
        :param hours: duration of the film
        :param director: director of the movie
        :param actors: actors in the movie
        :param link: link to the movie
        """
        # създавам конструктор с член променливи
        self.movie_name = movie_name
        self.year = year
        self.genre = genre
        self.rating = rating
        self.url_images = url_images
        self.hours = hours
        self.director = director
        self.actors = actors
        self.link = link

    def __str__(self):
        return f"Movie: {self.movie_name}, Year: {self.year}, Genre: {self.genre}, Rating: {self.rating}, " \
               f"Image: {self.url_images}, Hours: {self.hours}, Director: {self.director}, Actors: {self.actors}, " \
               f"Link: {self.link}"


Base.metadata.create_all(engine) # създава базата и колоните в нея