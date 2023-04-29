import datetime as dt
from flask import Flask, redirect, render_template
from flask_login import current_user, LoginManager, login_user, login_required, logout_user
from flask_restful import Api
from data import db_session, users_resources
from data.departments import Department
from data.users import User
from data.jobs import Jobs
from forms.department import AddDepForm
from forms.user import LoginForm, RegisterForm
from forms.job import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init('db/mars_explorer.db')
db_sess = db_session.create_session()

api = Api(app)


@login_manager.user_loader
def load_user(id_):
    return db_sess.get(User, id_)


def fullname(obj):
    if isinstance(obj, Jobs):
        worker = db_sess.get(User, obj.team_leader)
        return f'{worker.surname} {worker.name}'
    if isinstance(obj, Department):
        chief = obj.chief
        return f'{chief.surname} {chief.name}'


def get_members(dep):
    members_list = dep.members
    return ', '.join(f'{member.surname} {member.name}' for member in members_list)


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
        return redirect('/login/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login/', methods={'GET', 'POST'})
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return render_template('login.html', title='Авторизация', form=form, message='Пользователь не найден!')
        if not user.check_password(form.password.data):
            return render_template('login.html', title='Авторизация', form=form, message='Пароль неверный!')
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/job/add/', methods={'GET', 'POST'})
def add_job():
    form = AddJobForm()
    if form.validate_on_submit():
        team_leader = db_sess.get(User, form.team_leader.data)
        if not team_leader:
            return render_template('add_job.html', title='Добавление работы', form=form,
                                   message='Руководитель работы не найден')
        try:
            collaborators = [db_sess.get(User, id_) for id_ in map(int, form.collaborators.data.split(', '))]
            assert collaborators and all(collaborators)
        except (AssertionError, ValueError):
            return render_template('add_job.html', title='Добавление работы', form=form,
                                   message='Неправильное значение поля сотрудников')
        if form.start_date.data > form.end_date.data:
            return render_template('add_job.html', title='Добавление работы', form=form,
                                   message='Дата начала работы позже даты её окончания')
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job_desc.data,
            work_size=form.work_size.data,
            collaborators=collaborators,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
        )
        try:
            db_sess.add(job)
            db_sess.commit()
        except BaseException as err:
            db_sess.rollback()
            raise err
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы', form=form)


@app.route('/job/edit/<int:id_>', methods={'GET', 'POST'})
def edit_job(id_):
    form = AddJobForm()
    if form.validate_on_submit():
        job = db_sess.get(Jobs, id_)
        if not current_user.is_authenticated or job.team_leader not in {1, current_user.id}:
            return render_template('add_job.html', title='Редактирование работы', form=form,
                                   message='У вас нет прав на редактирование этой работы!')
        if not job:
            return render_template('add_job.html', title='')
        team_leader = db_sess.get(User, form.team_leader.data)
        if not team_leader:
            return render_template('add_job.html', title='Редактирование работы', form=form,
                                   message='Руководитель работы не найден')
        try:
            collaborators = [db_sess.get(User, id_) for id_ in map(int, form.collaborators.data.split(', '))]
            assert collaborators and all(collaborators)
        except (AssertionError, ValueError):
            return render_template('add_job.html', title='Редактирование работы', form=form,
                                   message='Неправильное значение поля сотрудников')
        if form.start_date.data > form.end_date.data:
            return render_template('add_job.html', title='Редактирование работы', form=form,
                                   message='Дата начала работы позже даты её окончания')
        try:
            job.team_leader = form.team_leader.data
            job.job = form.job_desc.data
            job.work_size = form.work_size.data
            job.collaborators = collaborators
            job.start_date = form.start_date.data
            job.end_date = form.end_date.data
            db_sess.commit()
        except BaseException as err:
            db_sess.rollback()
            raise err
        return redirect('/')
    return render_template('add_job.html', title='Редактирование работы', form=form)


@app.route('/job/delete/<int:id_>')
def delete_job(id_):
    job = db_sess.get(Jobs, id_)
    if not current_user.is_authenticated or (job and job.team_leader not in {1, current_user.id}):
        return render_template('error.html', title='Ошибка!', message='У вас нет прав на удаление этой работы!')
    if not job:
        return render_template('error.html', title='Ошибка!', message='Работа с указанным id не найдена!')
    try:
        db_sess.delete(job)
        db_sess.commit()
    except BaseException as err:
        db_sess.rollback()
        raise err
    return redirect('/')


@app.route('/departments/')
def departments():
    kwargs = {
        'title': 'List of departments',
        'departments': db_sess.query(Department).all(),
        'fullname': fullname,
        'get_members': get_members,
    }
    return render_template('departments.html', **kwargs)


@app.route('/department/add/', methods={'GET', 'POST'})
def add_department():
    form = AddDepForm()
    all_users = tuple(f'{user.surname} {user.name}' for user in db_sess.query(User).all())
    form.chief.choices = all_users
    form.members.choices = all_users
    if not current_user.is_authenticated or current_user.id != 1:
        return render_template('error.html', title='Ошибка!', message='У вас нет права на добавление департамента!')
    if form.validate_on_submit():
        chief_surname, chief_name = form.chief.data.split()
        chief = db_sess.query(User).filter((User.surname == chief_surname) & (User.name == chief_name)).first()
        if not chief:
            return render_template('add_department.html', title='Добавление департамента', form=form,
                                   message='Такой пользователь не найден!')
        members_fullnames = form.members.data
        members_list = []
        for member_surname, member_name in (s.split() for s in members_fullnames):
            member = db_sess.query(User).filter((User.surname == member_surname) & (User.name == member_name)).first()
            if not member:
                return render_template('add_department.html', title='Добавление департамента', form=form,
                                       message='Такой пользователь не найден!')
            members_list.append(member)
        dep = Department(
            title=form.title.data,
            chief_id=chief.id,
            email=form.email.data,
            members=members_list,
        )
        try:
            db_sess.add(dep)
            db_sess.commit()
        except BaseException as err:
            db_sess.rollback()
            raise err
        return redirect('/departments/')
    return render_template('add_department.html', title='Добавление департамента', form=form)


@app.route('/department/edit/<int:id_>', methods={'GET', 'POST'})
def edit_depatment(id_):
    form = AddDepForm()
    if not current_user.is_authenticated:
        return render_template('error.html', title='Ошибка!', message='Вы не авторизованы!')
    dep = db_sess.get(Department, id_)
    if current_user.id not in {dep.chief_id, 1}:
        return render_template('error.html', title='Ошибка!',
                               message='У вас нет права на редактирование этого департамента!')
    all_users = tuple(f'{user.surname} {user.name}' for user in db_sess.query(User).all())
    form.chief.choices = all_users
    form.members.choices = all_users
    if form.validate_on_submit():
        chief_surname, chief_name = form.chief.data.split()
        chief = db_sess.query(User).filter((User.surname == chief_surname) & (User.name == chief_name)).first()
        if not chief:
            return render_template('add_department.html', title='Редактирование департамента', form=form,
                                   message='Такой пользователь не найден!')
        members_fullnames = form.members.data
        members_list = []
        for member_surname, member_name in (s.split() for s in members_fullnames):
            member = db_sess.query(User).filter((User.surname == member_surname) & (User.name == member_name)).first()
            if not member:
                return render_template('add_department.html', title='Редактирование департамента', form=form,
                                       message='Такой пользователь не найден!')
            members_list.append(member)
        try:
            dep.title = form.title.data
            dep.chief_id = chief.id
            dep.email = form.email.data
            db_sess.commit()
        except BaseException as err:
            db_sess.rollback()
            raise err
        return redirect('/departments/')
    return render_template('add_department.html', title='Редактирование департамента', form=form)


@app.route('/department/delete/<int:id_>')
def delete_department(id_):
    dep = db_sess.get(Department, id_)
    if not dep:
        return render_template('error.html', title='Ошибка!', message='Департамент не найден!')
    try:
        db_sess.delete(dep)
        db_sess.commit()
    except BaseException as err:
        db_sess.rollback()
        raise err
    return redirect('/departments/')


@login_required
@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


def main():
    api.add_resource(users_resources.UsersListResource, '/api/v2/users')
    api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:user_id>')
    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
