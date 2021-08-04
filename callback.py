from dash.dependencies import Input, Output, State
from app import appDash
import dash
import dash_html_components as html
from app import dbDF
import pandas as pd
from datatables import UsersTable, ProjectsTable
@appDash.callback(
    Output('TableDB', 'data'),
    Output('TableDB', 'columns'),
    Output('RowCount', 'children'),
    Output('MonthFilter', 'disabled'),
    Output('DayFilter', 'disabled'),
    Output('MonthFilter', 'options'),
    Output('DayFilter', 'options'),
    Input('UserFilter', 'value'),
    Input('ProjectFilter', 'value'),
    Input('CustomerFilter', 'value'),
    Input('DayFilter', 'value'),
    Input('MonthFilter', 'value'),
    Input('YearFilter', 'value'),
    prevent_initial_call = True
)
def update_db(user, project, customer, day, month, year):
    from app import dbDF
    groupby = []
    df = dbDF
    monthD = True
    dayD = True

    if year is not None:
        groupby.append('ГОД')
        monthD = False
        if year != 'Все':
            df = df[(df['ГОД'] == year)]
    monthOp = [{'label': i, 'value': i} for i in df['ММ'].unique()] + [{'label': '✱', 'value': 'Все'}]
    if month is not None:
        groupby.append('ММ')
        dayD = False
        if month != 'Все':
            df = df[(df['ММ'] == month)]
    dayOp = [{'label': i, 'value': i} for i in df['ДД'].unique()] + [{'label': '✱', 'value': 'Все'}]
    if day is not None:
        groupby.append('ДД')
        if day != 'Все':
            df = df[(df['ДД'] == day)]

    if user is not None:
        groupby.append('СОТРУДНИК')
        if user != 'Все':
            df = df[(df['СОТРУДНИК'] == user)]

    if project is not None:
        if 'ПРОЕКТ' not in groupby:
            groupby.append('ПРОЕКТ')
        if 'ШИФР' not in groupby:
            groupby.append('ШИФР')
        if 'ЗАКАЗЧИК' not in groupby:
            groupby.append('ЗАКАЗЧИК')
        if project != 'Все':
            df = df[(df['ПРОЕКТ'] == project)]

    if customer is not None:
        if 'ПРОЕКТ' not in groupby:
            groupby.append('ПРОЕКТ')
        if 'ШИФР' not in groupby:
            groupby.append('ШИФР')
        if 'ЗАКАЗЧИК' not in groupby:
            groupby.append('ЗАКАЗЧИК')
        if customer != 'Все':
            df = df[(df['ЗАКАЗЧИК'] == customer)]

    if len(groupby) != 0:
        df = df.groupby(groupby)['ЧАСЫ'].sum().reset_index()
    try:
        df = df.sort_values('ГОД', ascending=False)
    except: pass

    cols = [{"name": i, "id": i} for i in df.columns]
    if df.shape[0] == 0:
        cols = [{"name": '⦰  ПУСТОЕ МНОЖЕСТВО', "id": 0}]
    return df.to_dict('records'), cols, [df.shape[0],html.Span('кол. строк', className='tail')], monthD, dayD, monthOp, dayOp

@appDash.callback(
    Output('UserFilter', 'value'),
    Output('ProjectFilter', 'value'),
    Output('CustomerFilter', 'value'),
    Output('DayFilter', 'value'),
    Output('MonthFilter', 'value'),
    Output('YearFilter', 'value'),
    Input('refresh', 'n_clicks'),
    prevent_initial_call = True
)
def cleanFilter(n_clicks):
    return None,None,None,None,None,None


@appDash.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-c':
        return html.Div([
            UsersTable()
        ], className='db')
    elif tab == 'tab-p':
        return html.Div([
            ProjectsTable()
        ], className='db')




