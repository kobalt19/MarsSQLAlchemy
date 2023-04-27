import datetime as dt
import flask
from flask_restful import abort, reqparse, Resource
from werkzeug.security import generate_password_hash
from . import db_session
from .users import User


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True, type=generate_password_hash)
parser.add_argument('created_date', required=True, type=lambda arg: dt.datetime.fromisoformat(arg))


class UsersResource(Resource):
    @staticmethod
    def get(user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return flask.jsonify({'user': {user.to_dict(only=('id', 'name'))}})

    @staticmethod
    def delete(user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class UsersListResource(Resource):
    @staticmethod
    def get():
        session = db_session.create_session()
        users = session.query(User).all()
        return flask.jsonify({'users': [user.to_dict() for user in users]})

    @staticmethod
    def post():
        session = db_session.create_session()
        args = parser.parse_args()
        user = User(
            name=args['name'],
            about=args['about'],
            email=args['email'],
            hashed_password=args['password'],
            created_date=args['created_date'],
        )
        session.add(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f'User {user_id} not found')
