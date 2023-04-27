import flask
from flask_restful import Api
from data import db_session, users_resources
from data.users import User

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/blogs.db')
db_sess = db_session.create_session()
api = Api(app)


def add_captain():
    captain = User(surname='Scott', name='Ridley', age=21, position='captain', speciality='research engineer',
                   address='module_1', email='scott_chief@mars.org')
    try:
        db_sess.add(captain)
        db_sess.commit()
    except BaseException as err:
        db_sess.rollback()
        raise err


def main():
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
    add_captain()
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
