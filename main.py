import flask
from flask_restful import Api
from data import db_session, users_resources
from data.users import User

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/mars.db')
db_sess = db_session.create_session()

api = Api(app)


def add_captain():
    user1 = User(
        surname='Scott',
        name='Ridley',
        age=21,
        position='captain',
        speciality='research engineer',
        address='module_1',
        email='scott_chief@mars.org'
    )
    user2 = User(
        surname='Weer',
        name='Andy',
        age=24,
        position='navigator',
        speciality='astrogeologist',
        address='module_1',
        email='weer_navigator@mars.org'
    )
    user3 = User(
        surname='Watney',
        name='Mark',
        age=20,
        position='steering',
        speciality='cyberengineer',
        address='module_2',
        email='watney_sttering@mars.org'
    )
    user4 = User(
        surname='Kapoor',
        name='Venkata',
        age=22,
        position='researcher',
        speciality='meteorologist',
        address='module_1',
        email='kapoor_researcher@mars.org'
    )
    try:
        for user in {user1, user2, user3, user4}:
            db_sess.add(user)
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
