import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

from sqlalchemy import Column, Integer, ForeignKey

#database_path = os.environ['DATABASE_URL']
database_path="postgresql://postgres:Test@123@localhost:5432/casting_agency"

db = SQLAlchemy()


# database_filename = "database.db"
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = f"sqlite:///{os.path.join(project_dir, database_filename)}"

# db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime)
    actors = db.relationship("Actor", secondary="MovieCast")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def add_movie_actors(self, actor_ids):
        movie_actors_objs = [
            MovieCast(movie_id=self.id, actor_id=actor_id)
            for actor_id in actor_ids
        ]

        db.session.add_all(movie_actors_objs)
        db.session.commit()

    def get_movie_actors(self):
        movie_cast = (
            MovieCast.query.filter_by(movie_id=self.id).join(Actor).all()
        )

        return movie_cast

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%d")
        }

    def __repr__(self):
        return json.dumps(self.format())


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    movies = db.relationship("Movie", secondary="MovieCast")

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
    def __repr__(self):
        return json.dumps(self.format())

    '''
    MovieCast
    This table allows the relationship between Movie and Actor
    '''
class MovieCast(db.Model):
    __tablename__ = 'MovieCast'

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('Movie.id'))
    actor_id = Column(Integer, ForeignKey('Actor.id'))
    movie = db.relationship(
        "Movie", backref=db.backref("MovieCast", cascade="all, delete-orphan")
    )
    actor = db.relationship(
        "Actor", backref=db.backref("MovieCast", cascade="all, delete-orphan")
    )

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_actors(cls, movie_id):
        results = cls.query.filter_by(movie_id=movie_id).all()
        return [result.actor_id for result in results]

    def short(self):
        return {"movie": self.movie.title, "actor": self.actor.name}

    def __repr__(self):
        return json.dumps(self.short())



