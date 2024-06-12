from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session
from data.groups import Groups
from data.person import Person
from data.teacher import Teacher
from data.lesson import Lesson
from data.attendance import Attendance
from data.forms import RegisterForm, LoginForm, PersonForm, GroupForm, LessonForm
#from get_vector import get_face_vector
import group_api
import groups_resorces

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Teacher).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Teacher).filter(Teacher.login == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        teacher = Teacher(
            login=form.login.data,
            name=form.name.data
        )
        teacher.set_password(form.password.data)
        db_sess.add(teacher)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)

@app.route("/", methods=['GET', 'POST'])
def start():
    return render_template('start.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Teacher).filter(Teacher.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            print(user.id)
            return redirect(url_for("index", user_id=user.id))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/<user_id>")
def index(user_id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        current_time = datetime.now()
        two_hours_ago = current_time - timedelta(hours= 2)
        lesson = db_sess.query(Lesson).filter(Lesson.teacher_id==user_id).first()
        if lesson:
            group = db_sess.query(Groups).filter(Groups.id == lesson.group_id).first()
            attendance_records = db_sess.query(Attendance, Person).join(Person).filter(Attendance.lesson_id == lesson.id).all()
            return redirect(url_for("check_lesson"))
        else:
            return redirect(url_for("add_lesson"))
    else:
        return redirect(url_for("login"))


@app.route('/add_group', methods=['GET', 'POST'])
@login_required
def add_group():
    form = GroupForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        group = Groups()
        group.name = form.name.data
        db_sess.add(group)
        db_sess.commit()
        return redirect(url_for("group_info", group_id=group.id))
    return render_template('add_group.html', form=form)
@app.route('/check_group', methods=['GET', 'POST'])
@login_required
def check_group():
    db_sess = db_session.create_session()
    group = db_sess.query(Groups)
    return render_template('check_group.html', group=group)
@app.route('/add_lesson', methods=['GET', 'POST'])
def add_lesson():
    form = LessonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        lesson = Lesson()
        lesson.teacher_id = form.teacher_id.data
        lesson.group_id = form.group_id.data
        db_sess.add(lesson)
        db_sess.commit()
        return redirect(url_for("video_feed"))
    return render_template('add_lesson.html', form=form)

@app.route('/check_lesson', methods=['GET', 'POST'])
def check_lesson():
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson)

    return render_template('check_lesson.html', lesson=lesson)
@app.route('/group/<group_id>', methods=['GET'])
def group_info(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Groups).filter(Groups.id == group_id).first()
    if not group:
        return "Группа не найдена", 404
    return render_template('group_info.html', group=group)


@app.route('/group/<group_id>/add_person', methods=['GET', 'POST'])
@login_required
def add_person(group_id):
    form = PersonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        person = Person()
        person.name = form.name.data

        if 'photo' in request.files:
            photo = request.files['photo']
            face_points = []

            # Сохранить вектор точек лица в базе данных
            person.face_vector = face_points

            db_sess.add(person)
            db_sess.commit()

            group = db_sess.query(Groups).filter(Groups.id == group_id).first()
            group.people.append(person)
            db_sess.commit()

            return redirect(url_for("group_info", group_id=group_id))
    return render_template('add_person.html', job='Добавление студента', form=form)


def main():
    db_session.global_init("db/people.db")
    app.register_blueprint(group_api.blueprint)

    # для списка объектов
    api.add_resource(groups_resorces.GroupsListResource, '/api/v2/groups')

    # для одного объекта
    api.add_resource(groups_resorces.GroupsResource, '/api/v2/groups/<int:groups_id>')

    app.run(debug=False)

if __name__ == "__main__":
    main()


