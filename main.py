from datetime import datetime, timedelta
from flask import Flask, render_template, redirect, request, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.groups import Groups
from data.person import Person
from data.teacher import Teacher
from data.lesson import Lesson
from data.attendance import Attendance
from data.forms import RegisterForm, LoginForm, PersonForm, GroupForm
#import dlib
#import cv2
#import numpy as np
#from ultralytics import YOLO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

# Инициализация моделей
#model = YOLO('data/model.pt')
#model.fuse()
#detector = dlib.get_frontal_face_detector()
#shape_predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
#face_rec_model = dlib.face_recognition_model_v1('data/dlib_face_recognition_resnet_model_v1.dat')


#def get_face_vector(frame):
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = detector(gray)
    #for face in faces:
       # shape = shape_predictor(gray, face)
        #face_descriptor = face_rec_model.compute_face_descriptor(frame, shape)
        #return np.array(face_descriptor)
    #return None

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
"""
@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Lesson).filter(Lesson.teacher_id != True)
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)"""
@app.route("/<user_id>")
def index(user_id):
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        current_time = datetime.now()
        two_hours_ago = current_time - timedelta(hours= 2)
        lesson = db_sess.query(Lesson).filter(Lesson.teacher_id==user_id, Lesson.start_time < current_time, Lesson.start_time > two_hours_ago).first()
        if lesson:
            group = db_sess.query(Groups).filter(Groups.id == lesson.group_id).first()
            attendance_records = db_sess.query(Attendance, Person).join(Person).filter(Attendance.lesson_id == lesson.id).all()
            return render_template("index.html", grop_name=group.name, attendance_records=attendance_records)
        else:
            return redirect(url_for("add_group"))
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
    return render_template('add_person.html', form=form)


@app.route('/group/<group_id>', methods=['GET'])
def group_info(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Groups).filter(Groups.id == group_id).first()
    if not group:
        return "Группа не найдена", 404
    return render_template('group_info.html', group=group)


@app.route('/<group_id>/add_person',  methods=['GET', 'POST'])
@login_required
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



if __name__ == "__main__":
    db_session.global_init("db/people.db")
    app.run(debug=False)
