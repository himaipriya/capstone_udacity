import os
from datetime import datetime
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS
from auth import requires_auth, AuthError
from models import setup_db, Actor, Movie


def create_app():
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return render_template("index.html", login_url=os.environ['LOGIN_URL'])

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PUT,POST,DELETE,PATCH,OPTIONS"
        )
        return response

    '''
    It fetches the list of available actors
    '''

    @app.route("/actors")
    @requires_auth("get:actors")
    def get_actors(jwt):
        try:
            actors = Actor.query.all()
            actors_list = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': actors_list
            })
        except 404:
            abort(404)

    '''
    Get Actor based on the id
    '''

    @app.route('/actors/<id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(jwt, id):
        try:
            actor = Actor.query.get(id)
            return jsonify({
                'success': True,
                'actor': actor.format()
            })
        except 404:
            abort(404)

    '''
    This allows you to create a new actor details
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):
        body = request.get_json()
        if not ('name' in body and 'age' in body and 'gender' in body):
            abort(422)
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')
        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'actor': [actor.format()]
            })
        except 422:
            abort(422)

    '''
    Update Actor information
    '''

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):
        actor = Actor.query.get(id)
        if actor:
            try:
                body = request.get_json()
                if 'name' in body:
                    actor.name = body.get('name')
                if 'age' in body:
                    actor.age = body.get('age')
                if 'gender' in body:
                    actor.gender = body.get('gender')
                actor.update()
                return jsonify({
                    'success': True,
                    'actors': actor.format()
                })
            except 422:
                abort(422)
        else:
            abort(404)

    '''
    Delete an actor
    '''

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.get(id)
        if actor:
            try:
                actor.delete()
                return jsonify({
                    'success': True,
                    'actors': id})
            except 422:
                abort(422)
        else:
            abort(404)

    '''
    Gets Movie List
    '''

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:
            movies = Movie.query.all()
            movie_list = [movie.format() for movie in movies]
            return jsonify({
                'success': True,
                'movies': movie_list
            })
        except 404:
            abort(404)

    '''
    Get Movie by Id
    '''

    @app.route('/movies/<id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(jwt, id):
        try:
            movie = Movie.query.get(id)
            return jsonify({
                'success': True,
                'movie': movie.format()
            })
        except 404:
            abort(404)

    '''
    Post a Movie
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):
        body = request.get_json()
        if not ('title' in body and 'release_date' in body):
            abort(422)
        try:
            title = body.get('title')
            release_date = body.get('release_date')
            release_date = datetime.strptime(release_date, "%Y-%m-%d")
            actor_ids = body.get('actor_ids')
            movie = Movie(title=title, release_date=release_date)
            if actor_ids:
                movie.add_movie_actors(actor_ids)
            movie.insert()
            return jsonify({
                'success': True,
                'movies': movie.format()
            })
        except 400:
            abort(400)

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):
        movie = Movie.query.get(id)
        if movie:
            try:
                body = request.get_json()
                if 'title' in body:
                    movie.title = body.get('title')
                if 'release_date' in body:
                    movie.release_date = datetime.strptime(body.get('release_date'), '%Y-%m-%d')
                movie.update()
                return jsonify({
                    'success': True,
                    'movies': [movie.format()]
                })
            except 400:
                abort(400)
        else:
            abort(404)

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if not movie:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            'movies': id
        })

    '''
    Error including 404 and 422.
     '''

    @app.errorhandler(404)
    def not_found(error):
        error_data = {
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }
        return jsonify(error_data), 404

    @app.errorhandler(422)
    def unprocessable(error):
        error_data = {
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }
        return jsonify(error_data), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        error_data = {
            "success": False,
            "error": error.status_code
        }
        return jsonify(error_data), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
