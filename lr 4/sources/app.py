import psycopg2
import requests
from flask import Flask, render_template, request, redirect

conn = psycopg2.connect(database="flask",
                        user="p.lysanov",
                        password=None,
                        host="localhost",
                        port="5432")

app = Flask(__name__)
app.debug = True

cursor = conn.cursor()

def is_number_in_string(string):
    for letter in string:
        if letter.isdigit():
            return [True, 'В имени недопустимы числа']
    return [False, None]

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if len(username) == 0 or len(password) == 0:
                return render_template('error.html', err_text='Логин или пароль не могут быть пустыми')
            cursor.execute("SELECT * FROM users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            if len(records) == 0:
                return render_template('error.html', err_text='Пользователь не найден')
            else:
                return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if len(name) == 0 or len(login) == 0 or len(password) == 0:
            return render_template('error.html', err_text='Пустые поля недопустимы')
        aboba = is_number_in_string(name)
        if aboba[0]:
            return render_template('error.html', err_text=aboba[1])
        cursor.execute("SELECT login FROM users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())
        if len(records) != 0:
            return render_template('error.html', err_text='Имя ' + str(login) + ' занято')
        else:
            cursor.execute('INSERT INTO users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
    return render_template('registration.html')