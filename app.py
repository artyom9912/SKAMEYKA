from flask import Flask
import flask_login
import dash
import json
import dash_bootstrap_components as dbc
import pandas as pd
from flask_caching import Cache
from sqlalchemy import create_engine

f = open('data.json')
config = json.load(f)
engine = create_engine(f'mysql+pymysql://{config["username"]}:{config["psswd"]}@{config["ip"]}/{config["db"]}')

# con = engine.connect()
app = Flask(__name__)
app.secret_key = b'_5f#cky2L"F4Q8z]/'

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
