from sys import getprofile
from turtle import title
from flask import Flask, render_template, url_for, session, abort, redirect, flash, g, request,send_file
from jinja2 import Template
import sqlite3
import os
import openpyxl
from FDataBase import FDataBase
from UserLogin import UserLogin
from werkzeug.security import generate_password_hash, check_password_hash
from FDataBase import FDataBase
from flask_login import LoginManager, login_user, login_required
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'.xls','.xlsx'}

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''база данных'''
DATABASE = 'archive.db'
DEBUG = True

app = Flask(__name__, template_folder='templates')#передает основной файл
app.config['SECRET_KEY'] = 'fhaks992jkjsjfuskakan'
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'archive.db')))

login_manager = LoginManager(app)

#Обработчик для авторизации

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)

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

'''Проверка есть ли соединение с БД'''
def get_db():
    if not hasattr(g, 'link_db'):# есть ли у обьекта g свойство link, тоесть соединение с базой данных
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

#Основная программа
auten = UserLogin.is_authenticated(login_user)
#Главная страница

@app.route("/main")
def index():
    print(auten)
    return render_template('index.html', menu = dbase.getMenu(), title = 'Главная') 
    

'''Разрыв соединения с БД'''
@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()

# Загрузка ексель файла


#Страница входа

@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = dbase.getUserByLogin(request.form['login'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            login_user(userlogin)
            return redirect(url_for('activ_requests'))
        flash("Неверно введен логин или пароль", "error")
 
    return render_template('login.html', title="Вход")

#Страница регистрации

@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        if len(request.form['login']) > 4 and len(request.form['password1']) > 4 \
                and request.form['password1'] == request.form['password2']:
            hash = generate_password_hash(request.form['password1'])
            res = dbase.addUser(request.form['login'], hash)
            if res:
                flash("ВЫ УСПЕШНО ЗАРЕГЕСТРИРОВАЛИСЬ!", "seccess")
                return redirect(url_for('login'))
            else:
                flash("ОШИБКА ПРИ ДОБАВЛЕНИИ В БД", "error")
        else:
            flash("НЕВЕРНО ВВЕДЕНЫ ДАННЫЕ", "error")
    return render_template('registration.html', title = 'Регистрация')

#Страница запросов

@app.route("/addrequest", methods=["POST", "GET"])
@login_required
def addrequest():
    if request.method == "POST":
        if len(request.form['last_name']) > 4 :
            res = dbase.addrequest(request.form['pp'], request.form['last_name'],
            request.form['first_name'], request.form['o_name'], 
            request.form['d_name'], request.form['date_n'],
            request.form['date_k'],request.form['date_b'])
            if not res:
                flash('Ошибка добавления запроса', category = 'error')
            else:
                flash('Запрос добавлен успешно', category='success')
        else:
            flash('Ошибка добавления запроса', category='error')
    return render_template('addrequest.html', menu = dbase.getMenu(), title = 'Добавить запрос' )

#Отображение активных запросов

@app.route("/activ_requests", methods=["POST", "GET"])
@login_required
def activ_requests():
    return render_template('activ_requests.html', menu = dbase.getMenu(), title = 'Активные запросы',requests = dbase.getRequestsAnons())

#Отображение выполненых запросов

@app.route("/сompleted_requests", methods=["POST", "GET"])
@login_required
def сompleted_requests():
    return render_template('сompleted_requests.html', menu = dbase.getMenu(), title = 'Выполненные запросы')

#Показ запросов
    
@app.route("/ShowRequests/<int:id_request>")
@login_required
def showRequests(id_request):
    last_name, first_name, o_patronymic, d_position = dbase.getInfoEmployeesRequests(id_request)
    pp, data_nach, data_kon, data_tek = dbase.getInfoAddRequests(id_request)
    profile = dbase.getProfileAnons(id_request)
    if not title:
        abort(404)
 
    return render_template('ShowRequests.html', menu=dbase.getMenu(), title='Запрос '+ last_name + " " + first_name, 
    last_name = last_name, first_name=first_name, o_patronymic= o_patronymic, d_position=d_position,
    pp = pp, data_nach = data_nach, data_kon = data_kon, data_tek = data_tek, profile=profile,
    order = dbase.getOrdersAnons(id_request),
    calc_month = dbase.getCalc_MonthAnons(profile)
    )



#Страница приема документов
@app.route('/download_file')
def download_file():
    return send_file('Шаблон приема документов.xlsx')
   

@app.route("/acceptance", methods=["POST", "GET"])
@login_required
def acceptance():

    if request.method == 'POST':

        if 'file' not in request.files: 
            print('Не могу прочитать файл')
        else:    
            file = request.files['file']
            filename = secure_filename(file.filename)
            if file.filename == '':
                flash('Нет выбранного файла')
            else:
                dbase.getListInventories(filename)
        
    return render_template('acceptance.html', menu = dbase.getMenu(), title = 'Прием документов', doc = dbase.getDocumentsAnons(),
    inv_id = dbase.getInventories_id())


# Утилизация документов
@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    
    return render_template('doc_delete.html', menu = dbase.getMenu(), title = 'Утилизация документов', doc = dbase.getDocumentsDeleteAnons(),
    doc_del = dbase.getDocumentsdelite())


# Составить акт утилизации
@app.route("/download_act_delete")
@login_required
def download_act_delete():
    doc_del = dbase.getDocumentsdelite()
    act = dbase.getExelDocumentsdelite(doc_del)
    if act:
        dbase.DeletAcceptance(doc_del)
    return send_file(act)

#Приказы и лицевые счета
#Шаблон приказов
@app.route('/download_orders_file')
def download_orders_file():
    return send_file('Шаблон добавления приказов.xlsx')

#приказы
@app.route("/orders", methods=["POST", "GET"])
@login_required
def orders():
    if request.method == 'POST':
        if 'file' not in request.files: 
            print('Не могу прочитать файл')
        else:    
            file = request.files['file']
            filename = secure_filename(file.filename)
            print(filename)
            if file.filename == '':
                flash('Нет выбранного файла')
            else:
                dbase.getExeleOrders(filename)

    return render_template('orders.html', menu = dbase.getMenu(), title = 'Приказы', orders = dbase.getListOrders(),
    employee = dbase.getAllEmployee())

#Шаблон добавления лицевых счетов
@app.route('/download_personal_accounts_file')
def download_personal_accounts_file():
    return send_file('Шаблон добавления лицевых счетов.xlsx')

#Лицевые счета
@app.route("/personal_accounts", methods=["POST", "GET"])
@login_required
def personal_accounts():
    if request.method == 'POST':
        if 'file' not in request.files: 
            print('Не могу прочитать файл')
        else:    
            file = request.files['file']
            filename = secure_filename(file.filename)
            print(filename)
            if file.filename == '':
                flash('Нет выбранного файла')
            else:
                dbase.getExelepersonal_accounts(filename)

    return render_template('personal_accounts.html', menu = dbase.getMenu(), title = 'Лицевые счета',
    employee = dbase.getAllEmployee(), profile = dbase.getListProfile(), calc_month = dbase.getListCalc_Month())

@app.route("/listemployee", methods=["POST", "GET"])
@login_required
def listemployee():
    serch = ''
    opred = 0
    e = dbase.getAllEmployee()
    if request.method == "POST":
        serch = request.form ['s']
        print(serch)
        if serch != '':
            e = dbase.getAllEmployeeSerch(serch)
            opred = 1
    
    return render_template('listemployee.html', menu = dbase.getMenu(), title = 'Список сотрудников',
    employee = e, opred = opred)



@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=dbase.getMenu())



if __name__ == "__main__":
    app.run(debug=True)

