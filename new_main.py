from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, session, request, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.groups import Groups
from data.person import Person
from data.teacher import Teacher
from data.lesson import Lesson
from data.attendance import Attendance
from data.forms import RegisterForm, LoginForm, PersonForm, GroupForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
teac_id = None

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
        if 'user_id' in session:
            user_id = session['user_id']
        user = db_sess.query(Teacher).filter(Teacher.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return render_template('lesson.html')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)



@app.route('/lesson', methods=['GET', 'POST'])
def lesson_check():
    global teac_id
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.teacher_id == 1)
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("lesson.html", lesson=lesson)

@app.route("/add_group", methods=['GET', 'POST'])
def add_group():
    form = GroupForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        group = Groups()
        group.name = form.name.data
        db_sess.add(group)
        db_sess.commit()
        return redirect(url_for("group_info", group_id=group.id))
    return render_template('create_group.html', form=form)

@app.route("/check_group", methods=['GET', 'POST'])
def check_group():
    db_sess = db_session.create_session()
    group = db_sess.query(Groups)
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("check_group.html", group=group)

@app.route('/check_group/<group_id>', methods=['GET', 'POST'])
def add_jobs(group_id):
    form = PersonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        person = Person()
        person.name = form.name.data
        db_sess.add(person)
        db_sess.commit()

        group = db_sess.query(Groups).filter(Groups.id == group_id).first()
        group.people.append(person)
        db_sess.commit()

        return redirect(url_for("group_info", id=group_id))
    return render_template('add_person.html', job='Добавление студента', form=form)



@app.route('/group/<group_id>', methods=['GET'])
def group_info(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Groups).filter(Groups.id == group_id).first()
    if not group:
        return "Группа не найдена", 404
    return render_template('group_info.html', group=group)
if __name__ == "__main__":
    db_session.global_init("db/people.db")
    app.run(port=8080, host='127.0.0.1', debug=False)