from flask import Flask
import flask_login
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache
# from clickhouse_driver import connect
from sqlalchemy import create_engine
# from flaskext.mysql import MySQL
# con = connect('clickhouse://10.200.2.113')
engine = create_engine('mysql+pymysql://root:root@127.0.0.1/skameyka')
# con = engine.connect()
app = Flask(__name__)
app.secret_key = b'_5f#cky2L"F4Q8z]/'

# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_DB'] = 'skameyka'
# mysql = MySQL()
# mysql.init_app(app)
# con = mysql.get_db()

WEEKDAYS= ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
calendar_cache = []
dbDF=[pd.DataFrame(),]


appDash = dash.Dash(__name__,
                     server=app,
                     url_base_pathname='/dash/',
                    external_stylesheets=[dbc.themes.BOOTSTRAP],
                    suppress_callback_exceptions=True)
cache = Cache(appDash.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# dbDF = pd.read_excel('db.xlsx')
# usersDF = pd.read_excel('users.xlsx')
# prjsDF = pd.read_excel('projects.xlsx')
