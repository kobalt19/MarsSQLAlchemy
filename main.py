import datetime as dt
from flask import Flask, redirect, render_template
from flask_restful import Api
from data import db_session, users_resources
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

db_session.global_init('db/mars_explorer.db')
db_sess = db_session.create_session()

api = Api(app)


def fullname(job):
    worker = db_sess.get(User, job.team_leader)
    return f'{worker.surname} {worker.name}'


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


def add_job():
    first_job = Jobs(
        team_leader=1,
        job='deployment of residential modules 1 and 2',
        work_size=15,
        collaborators='2, 3',
        start_date=dt.datetime.now(),
    )
    try:
        db_sess.add(first_job)
        db_sess.commit()
    except BaseException as err:
        db_sess.rollback()
        raise err


@app.route('/')
@app.route('/index')
def index():
    works_list = db_sess.query(Jobs).all()
    kwargs = {
        'title': 'Works log',
        'works_list': works_list,
        'fullname': fullname,
    }
    return render_template('index.html', **kwargs)


@app.route('/register/', methods={'POST', 'GET'})
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message='Пароли не совпадают!', title='Регистрация')
        if db_sess.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', form=form, message='Такой пользователь уже есть!',
                                   title='Регистрация')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data,
        )
        user.set_password(form.password.data)
        try:
            db_sess.add(user)
            db_sess.commit()
        except BaseException as err:
            db_sess.rollback()
            raise err
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
