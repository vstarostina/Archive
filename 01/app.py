import sqlite3
import os
from FDataBase import FDataBase
from UserLogin import UserLogin
from flask import Flask, render_template, url_for, request, redirect, flash, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required


DATABASE = 'archive.db'
DEBUG = True

app = Flask(__name__)#передает основной файл
app.config['SECRET_KEY'] = 'fhaks992jkjsjfuskakan'
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'archive.db')))

login_manager = LoginManager(app)


#____Создание базы данных
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row #представление не в виде кортежей
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):# есть ли у обьекта g свойство link, тоесть соединение с базой данных
        g.link_db = connect_db()
    return g.link_db

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user = dbase.getUserByLogin(request.form['login'])

        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('about'))
        flash("Неверно введен логин или пароль", "error")
    return render_template('index.html')


@app.teardown_appcontext# разрыв соединения с БД
def close_db(error):
    '''Закрываем соединение с БД если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/profil')
@login_required
def profil():
    return render_template('profil.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['login']) > 4 and len(request.form['password']) > 4 \
                and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['login'], hash)
            if res:
                flash("ВЫ УСПЕШНО ЗАРЕГЕСТРИРОВАЛИСЬ!", "seccess")
                return redirect('/')
            else:
                flash("ОШИБКА ПРИ ДОБАВЛЕНИИ В БД", "error")
        else:
            flash("НЕВЕРНО ВВЕДЕНЫ ДАННЫЕ", "error")

    return render_template('register.html')


@app.route('/credit', methods=['POST', 'GET'])
def credit():
    if request.method == 'POST':
        if len(request.form['text']) > 4:
            res = dbase.addPost(request.form['text'], request.form['sum'])
            if res:
                flash("ВЫ УСПЕШНО ВЗЯЛИ КРЕДИТ!", "seccess")
                return redirect('/about')
            else:
                flash("ОШИБКА ПРИ ДОБАВЛЕНИИ В БД", "error")
        else:
            flash("НЕВЕРНО ВВЕДЕНЫ ДАННЫЕ", "error")

    return render_template('credit.html')


if __name__ == "__main__":
    app.run(debug=True)