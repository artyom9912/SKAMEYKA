from flask import Flask, render_template, request, redirect, flash
# from flaskext.mysql import MySQL
import flask_login
from flask_login import login_required
from user import User
import pandas as pd
import dash
from view import LAYOUT, PROJECTDESK, CALENDAR
from view_specials import DATABASE, ADMINPAGE
from dash.dependencies import Input, Output

from callback import update_db
from app import appDash, app, calendar_cache, login_manager, engine, dbDF
# from clickhouse_driver import connect
# CLICKHOUSE_ENGINE = create_engine('clickhouse://10.200.2.113/recengine')


@login_manager.user_loader
def loadUser(user_id):
    con = engine.connect()
    # con = connect('clickhouse://10.200.2.113')
    res = con.execute(f'SELECT id, username, relevant, admin, fullname FROM skameyka.user_table WHERE id = {user_id}')
    user=res.fetchone()
    print(user)
    if user is None: return
    USER = User()
    USER.id = user[0]
    USER.userName = user[1]
    USER.relevant = user[2]
    USER.admin = user[3]
    USER.name = user[4]
    return USER

@app.route('/')
@login_required
def main():
    user = flask_login.current_user.name
    return redirect('/dash/')

@app.route('/loginpage')
def loginpage():
    return render_template('login.html')
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/loginpage')

@app.route('/login', methods=['POST'])
def login():
    con = engine.connect()
    # con = connect('clickhouse://10.200.2.113')
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    if password == '' or username == '':
        flash('Не все поля были заполнены!')
        return redirect('/loginpage')
    # con = mysql.get_db()
    # cursor = con.cursor()
    res = con.execute(f'SELECT id, password FROM skameyka.user_table '
                   f'WHERE relevant = 1 AND username like \'{username}\';')
    row = res.fetchone()
    if row is None:
        flash('Такого пользователя нет!')
        return redirect('/loginpage')
    psswd = row[1]
    if password != psswd:
        flash('Неверный пароль! Попробуйте снова')
        return redirect('/loginpage')
    id = row[0]
    user = loadUser(user_id=id)
    flask_login.login_user(user, remember=remember)
    return redirect('/')

@app.login_manager.unauthorized_handler
def unathor():
    return redirect('/loginpage')

#------------DASH---------------
appDash.layout = LAYOUT('', '')
appDash.title = 'SKMK'
@app.route('/dash')
@flask_login.login_required
def projectDesk():
    # username = flask_login.current_user.name
    # role = 'Администратор' if flask_login.current_user.admin == 1 else 'Сотрудник'
    # appDash.layout = PROJECTDESK(username,role)
    return appDash.index()
# @app.route('/calendar')
# # @flask_login.login_required
# def calendar():
#     return appDash.index()

@appDash.callback(Output('content', 'children'),
              Input('prjBtn', 'n_clicks'),
              Input('calBtn', 'n_clicks'),
              Input('dbBtn', 'n_clicks'),
              Input('admBtn', 'n_clicks'))
def display_page(prjBtn, calBtn, dbBtn, admBtn):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    con = engine.connect()
    global dbDF
    for i in range(0,len(calendar_cache)): del calendar_cache[0]

    if 'prjBtn' in changed_id:
        content = PROJECTDESK()
    elif 'calBtn' in changed_id:
        content = CALENDAR()
    elif 'dbBtn' in changed_id:
        dbDF[0]=(pd.read_sql("""
        SELECT YEAR(timestamp), MONTH(timestamp), DAY(timestamp), fullname, title, code, customer, hours
        FROM skameyka.main_table
        JOIN skameyka.project_table ON project_table.id = project_id
        JOIN skameyka.user_table ON user_table.id = user_id
        ORDER BY timestamp desc
    """, con))
        head = ['ГОД', 'ММ', 'ДД', 'СОТРУДНИК', 'ПРОЕКТ', 'ШИФР', 'ЗАКАЗЧИК', 'ЧАСЫ']
        dbDF[0].columns = head
        print(dbDF[0].shape)
        content = DATABASE(dbDF[0])
    elif 'admBtn' in changed_id:
        content = ADMINPAGE()
    else:
        content = ADMINPAGE()
    return content

if __name__ == '__main__':
    app.run(host='localhost',port=80, debug=True)
