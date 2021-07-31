import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import dash
import plotly.graph_objects as go
import pandas as pd
from app import dbDF

filterItems = [
    dbc.DropdownMenuItem("Актуальные"),
    dbc.DropdownMenuItem("Архивные"),
    dbc.DropdownMenuItem("Все"),
]
def DATABASE():
    global dbDF
    dbDF['ШИФР'] = dbDF['ШИФР'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        html.Div('БАЗА ДАННЫХ', className='name'),
        html.Div([
            dcc.Loading([
            dash_table.DataTable(
                id='TableDB',
                data=dbDF.to_dict('records'),
                columns=[{"name": i, "id": i} for i in dbDF.columns],
                fixed_rows={'headers': True, 'data': 0},
                style_data={
                    'whiteSpace':'normal'
                },
                style_table={
                    'overflow': 'hidden',
                    'margin': '0',
                    'margin-top': '0px',
                    'padding': '0',
                    'width': '100%',
                    'height': '100%',
                    'min-height':'400px',
                    'max-height':'72vh',
                    'overflow-y':'auto',
                    'border': '0px solid white',
                    'borderRadius': '10px',
                    'minWidth': '100%',
                },
                style_cell={'font-family': 'Rubik', 'text-align': 'left', 'width':'auto',
                            'border': '2px solid white', 'background-color': '#f7f7f7',
                            'font-size': '14px', 'padding-left':'12px', 'cursor':'default'},
                style_header={'background-color': '#313131', 'color': 'white', 'height': '35px','z-index':'5',
                              'border': '0px solid white', 'font-family': 'Rubik', 'font-size': '14px'},
                style_data_conditional=[
                    {
                        "if": {"state": "selected"},  # 'active' | 'selected'
                        "backgroundColor": "rgba(0, 116, 217, 0.3)",
                        'border': '2px solid white',
                    },
                ],
                style_cell_conditional=[
                    {
                        'if': {'column_id': 'ЧАСЫ'},
                        'textAlign': 'center',
                        'background-color': '#F0F0F0',
                        'padding-left': '0',
                        'width': '100px',
                        # 'max-width': '60px',
                    },
                ],
            )], color='grey', type='circle'),
        ], className='db line'),
        html.Div([
        html.Div([
            html.Div('Настройки', style={'margin-bottom': '10px'}),
            dbc.Form([
            dcc.Dropdown(id='DayFilter', placeholder='ДД', style={'width':'70px', 'margin-right':'6px'}, disabled=True,
                         options=[{'label': i, 'value': i} for i in dbDF['ДД'].unique()]+[{'label': '✱', 'value': 'Все'}]),
            dcc.Dropdown(id='MonthFilter', placeholder='ММ', style={'width':'70px', 'margin-right':'6px'}, disabled=True,
                         options=[{'label': i, 'value': i} for i in dbDF['ММ'].unique()]+[{'label': '✱', 'value': 'Все'}], ),
            dcc.Dropdown(id='YearFilter', placeholder='ГОД', style={'width':'85px', 'margin-right':'6px'},
                         options=[{'label': i, 'value': i} for i in dbDF['ГОД'].unique()]+[{'label': '✱', 'value': 'Все'}], ),], inline=True),
            dcc.Dropdown(id='UserFilter',placeholder='Сотрудник', options=[{'label': i, 'value': i} for i in dbDF['СОТРУДНИК'].unique()]+[{'label': '[Все сотрудники]', 'value': 'Все'}]),
            dcc.Dropdown(id='ProjectFilter',placeholder='Проект', options=[{'label': i, 'value': i} for i in dbDF['ПРОЕКТ'].unique()]+[{'label': '[Все проекты]', 'value': 'Все'}]),
            dcc.Dropdown(id='CustomerFilter',placeholder='Заказчик', options=[{'label': i, 'value': i} for i in dbDF['ЗАКАЗЧИК'].unique()]+[{'label': '[Все заказчики]', 'value': 'Все'}]),
        ], className='cloud'),
        html.Button('Сбросить', className='clean', id='refresh')
        ], className='filters line'),
        html.Div([dbDF.shape[0], html.Span('кол. строк', className='tail')],id='RowCount', className='cloud number rows'),
    ])
    return content

def ADMINPAGE():
    content = html.Div([
        html.Div('АДМИНИСТРИРОВАНИЕ', className='name'),
        html.Div([
            dcc.Tabs(id='tabs', value='tab-c', children=[
                dcc.Tab(label='Сотрудники', value='tab-c', className='custom-tab', selected_className='custom-tab--selected'),
                dcc.Tab(label='Проекты', value='tab-p', className='custom-tab', selected_className='custom-tab--selected'),
            ], parent_className='custom-tabs', className='custom-tabs-container',),
        ], className='cloud tablo'),
        dcc.Loading([html.Div(id='tabs-content')],color='grey', type='circle')
    ])
    return content
