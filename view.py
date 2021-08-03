import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import pandas as pd
from view_specials import DATABASE

filterItems = [
    dbc.DropdownMenuItem("Актуальные"),
    dbc.DropdownMenuItem("Архивные"),
    dbc.DropdownMenuItem("Все"),
]
Years= [
    dbc.DropdownMenuItem("2021"),
    dbc.DropdownMenuItem("2020"),
    dbc.DropdownMenuItem("2019"),
    dbc.DropdownMenuItem("Всё время"),
]

def LAYOUT(username, role):
    layout = html.Div([dcc.Location(id='url', refresh=False),
        dbc.Row([
            html.Div([
                html.Div([
                    html.Img(src='assets/img/user.png', className='userPic'),
                    html.Div(username, className='userName'),
                    html.Div(role, className='userRole'),
                ],className='userBox'),
                html.Div([
                    html.A(html.Button([
                        html.Span([], className='ico1'), 'Доска проектов',
                    ], className='button option'), id='prjBtn', n_clicks=0),
                    html.A(html.Button([
                        html.Span([], className='ico2'), 'Календарный отчёт',
                    ], className='button option'), id='calBtn', n_clicks=0),
                    html.A(html.Button([
                        html.Span([], className='ico3'), 'База данных',
                    ], className='button option'), id='dbBtn', n_clicks=0),
                    html.A(html.Button([
                        html.Span([], className='ico4'), 'Администрация',
                    ], className='button option'), id='admBtn', n_clicks=0)
                ], className='options')
            ], className='side menu'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(src='assets/img/logo.png', className='logo'),
                        html.Div([
                            html.Div(['ENTERPRISE'], className='title'),
                            html.Div(['recourse management'], className='subtitle')
                        ], className='titleBox'),
                    ], className='banner'),
                    html.Div([
                        html.A(
                        html.Button([
                            html.Span([], className='icon1'),'Обновить'
                        ],className='button'),href='/dash/'),
                        html.A(html.Button([
                            html.Span([], className='icon2'),'Выйти',
                        ], className='button exit'), href='/logout')
                    ],className='buttons')
                ], className='header'),
                #-------------CONTENT-------------#
                # dcc.Loading([
                html.Div([],
                className='content', id='content')
                # ], color='grey', type='circle'),
            ], className='side main')
        ])
    ])
    return layout


def PROJECTDESK():
    content = html.Div(
        [
        html.Div('ДОСКА ПРОЕКТОВ', className='name'),
        html.Div([
            html.Div([47, html.Span('завершено', className='tail')], className='cloud number line'),
            html.Div([12, html.Span('актуальных', className='tail')], className='cloud number line'),
            ], className='line-wrap'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(['ЖК АКВАМАРИН', dcc.Markdown('**Этап: **' + 'подготовка', className='prjStage')],
                                 className='prjName'),
                        html.Div([
                            html.Div([62, html.Span('часа', className='tail')], className='num line'),
                            html.Div([9, html.Span('сотрудников', className='tail')], className='num line dim'),
                        ], className='line-wrap prjInfo'),
                    ], className='card'),
                    html.Div([
                        html.Div(['ЖК АКВАМАРИН',
                                  dcc.Markdown('**Этап: **' + 'реализация', className='prjStage')],
                                 className='prjName'),
                        html.Div([
                            html.Div([53, html.Span('часа', className='tail')], className='num line'),
                            html.Div([4, html.Span('сотрудников', className='tail')],
                                     className='num line dim'),
                        ], className='line-wrap prjInfo'),
                    ], className='card'),
                    html.Div([], className='card'),
                    html.Div([], className='card'),
                ], className='grid'),
            ], className='cloud desk line'),
            html.Div([
                html.Div('Фильтры', className='silence',),
                dbc.DropdownMenu(label="Актуальные", bs_size="md", color='white', children=filterItems),
                dbc.DropdownMenu(label="2021", bs_size="md", color='white', children=Years),
            ], className='cloud filter line'),
        ], className='line-wrap focus'),])
    return content

def CALENDAR():
    colors = ['#393E46', '#00ADB5','#AAD8D3','#EEEEEE','#8ee8e4', '#F3F4ED', '#30475E','4CA1A3']
    df = pd.read_excel('cal.xlsx')
    mart = df.fillna(0)
    mart['sum'] = mart['ПН']+mart['ВТ']+mart['СР']+mart['ЧТ']+mart['ПТ']+mart['СБ']+mart['ВС']
    mart = mart[['НАЗВАНИЕ ПРОЕКТА','sum']]
    labels = mart['НАЗВАНИЕ ПРОЕКТА'].tolist()
    values = mart['sum'].tolist()
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)],)
    fig.update_traces(automargin=False, selector = dict(type='pie'),
                      marker=dict(colors=colors), textfont_size=12,
                      hoverinfo='label+percent', textinfo='none')
    fig.update_layout(
        font_family="Roboto",
        font_color="black",
        font_size=16,
        margin=dict(l=4, r=12, t=20, b=40),
        height = 280,
        width= 410,
        legend=dict(font=dict(family="Rubik", size=12, color="black")),
        hoverlabel=dict(
            font_size=14,
            font_family="Rubik",
        )
    )

    content = html.Div(
        [
        html.Div('МОДУЛЬ КАЛЕНДАРЬ', className='name'),
        html.Div([
            html.Div(['Июль', html.Span('2021 год', className='tail')], className='cloud number line'),
            ], className='line-wrap'),
        html.Div([
            html.Div([
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in df.columns],
                    id='CalendarTable',
                    css='.dash-cell{background-color: #37bc8d !important; }',
                    editable=True,
                    style_table={
                        # 'border': '1px solid red',
                        'overflow': 'hidden',
                        'margin': '0',
                        'margin-top': '-5px',
                        'padding': '0',
                        'width' : '100%',
                        'height': '400px',
                        'border': '0px solid white',
                        'borderRadius': '20px',
                    },
                    style_cell={'font-family':'Rubik', 'text-align':'center',
                                'border': '2px solid white', 'background-color':'#f7f7f7',
                                'font-size':'16px', },
                    style_header={'background-color':'#313131', 'color':'white', 'height':'41px',
                                  'border': '0px solid white','font-family':'Roboto','font-size':'18px'},
                    style_data_conditional=[
                        {
                            "if": {"state": "selected"},  # 'active' | 'selected'
                            "backgroundColor": "rgba(0, 116, 217, 0.3)",
                            'border': '2px solid white',
                        },
                    ],
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'textAlign': 'left',
                            'background-color': '#eaeaea',
                            'padding-left': '25px'
                        } for c in ['НАЗВАНИЕ ПРОЕКТА']
                    ],
                    style_header_conditional=[
                        {
                            'if': {'column_id': c},
                            'background-color': '#00ADB5',
                            # 'border': '2px solid #474747',
                        } for c in ['ПТ']
                    ]
                )
            ], className='calendar line'),
            html.Div([
                dcc.Loading(
                dcc.Graph(
                    id="pie-chart",
                    figure= fig,
                    config={'displayModeBar': False},
                ), color='grey', type='circle'),
            ], className='cloud line', style={'height':'fit-content','border-radius':'25px'}),
        ], className='line-wrap focus'),])
    return content

