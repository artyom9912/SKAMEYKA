from flask import Flask
import flask_login
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from flaskext.mysql import MySQL
app = Flask(__name__)
app.secret_key = b'_5f#cky2L"F4Q8z]/'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'skameyka'
mysql = MySQL()
mysql.init_app(app)
appDash = dash.Dash(__name__,
                     server=app,
                     url_base_pathname='/dash/',
                    external_stylesheets=[dbc.themes.BOOTSTRAP])

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

dbDF = pd.read_excel('db.xlsx')
usersDF = pd.read_excel('users.xlsx')
prjsDF = pd.read_excel('projects.xlsx')
con = mysql.get_db()
