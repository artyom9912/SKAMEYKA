from flask import Flask, render_template, request, redirect, flash
# from flaskext.mysql import MySQL
import flask_login
from flask_login import login_required
from user import User
import dash
from view import LAYOUT, PROJECTDESK, CALENDAR
from view_specials import DATABASE, ADMINPAGE
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from callback import update_db
from app import appDash, app, login_manager#, mysql

# from app import con
#
# @login_manager.user_loader
# def loadUser(user_id):
#     con = mysql.get_db()
#     cursor = con.cursor()
#     cursor.execute(f'SELECT id, UserName, isRelevant, isAdmin, Name FROM user_table WHERE id = {user_id}')
#     user=cursor.fetchone()
#     if user is None: return
#     USER = User()
#     USER.id = user[0]
#     USER.userName = user[1]
#     USER.relevant = user[2]
#     USER.admin = user[3]
#     USER.name = user[4]
#     return USER
#
# @app.route('/')
# @login_required
# def hello_world():
#     user = flask_login.current_user.name
#     return redirect('/dash/')
#
# @app.route('/loginpage')
# def loginpage():
#     return render_template('login.html')
# @app.route('/logout')
# def logout():
#     flask_login.logout_user()
#     return redirect('/loginpage')
#
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False
#     if password == '' or username == '':
#         flash('Не все поля были заполнены!')
#         return redirect('/loginpage')
#     con = mysql.get_db()
#     cursor = con.cursor()
#     cursor.execute(f'SELECT id, password FROM user_table WHERE username like \'{username}\';')
#     row = cursor.fetchone()
#     if row is None:
#         flash('Такого пользователя нет!')
#         return redirect('/loginpage')
#     psswd = row[1]
#     if password != psswd:
#         flash('Неверный пароль! Попробуйте снова')
#         return redirect('/loginpage')
#     id = row[0]
#     user = loadUser(user_id=id)
#     flask_login.login_user(user, remember=remember)
#     return redirect('/')
#
# @app.login_manager.unauthorized_handler
# def unathor():
#     return redirect('/loginpage')

#------------DASH---------------
appDash.layout = LAYOUT('Бурлака Евгений', 'Администратор')
appDash.title = 'Проекты'
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
    if 'prjBtn' in changed_id:
        content = PROJECTDESK()
    elif 'calBtn' in changed_id:
        content = CALENDAR()
    elif 'dbBtn' in changed_id:
        content = DATABASE()
    elif 'admBtn' in changed_id:
        content = ADMINPAGE()
    else:
        content = PROJECTDESK()
    return content

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80, debug=False)
