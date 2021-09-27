import datetime
from datetime import datetime as dt
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from app import appDash, calendar_cache, engine, WEEKDAYS
import dash
from time import sleep
import dash_html_components as html
import traceback
import sys
import pandas as pd
import plotly.graph_objects as go
import flask_login
from datatables import UsersTable, ProjectsTable

WEEK_NUMBERS = dict(zip(WEEKDAYS, range(0, 7)))
precalendar = pd.DataFrame()

@appDash.callback(
    Output('USER', 'children'),
    Output('ROLE', 'children'),
    Input('content', 'children')
)
def SetUser(style):
    print()
    return flask_login.current_user.name, 'Администратор' if flask_login.current_user.admin == 1 else 'Сотрудник'


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
    prevent_initial_call=True
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
    except:
        pass

    cols = [{"name": i, "id": i} for i in df.columns]
    if df.shape[0] == 0:
        cols = [{"name": '⦰  ПУСТОЕ МНОЖЕСТВО', "id": 0}]
    return df.to_dict('records'), cols, [df.shape[0],
                                         html.Span('кол. строк', className='tail')], monthD, dayD, monthOp, dayOp


@appDash.callback(
    Output('UserFilter', 'value'),
    Output('ProjectFilter', 'value'),
    Output('CustomerFilter', 'value'),
    Output('DayFilter', 'value'),
    Output('MonthFilter', 'value'),
    Output('YearFilter', 'value'),
    Input('refresh', 'n_clicks'),
    prevent_initial_call=True
)
def cleanFilter(n_clicks):
    return None, None, None, None, None, None


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


calendar = None


@appDash.callback(
    Output('Datepicker', 'date'),
    Output('EndDate', 'children'),
    Output('CalendarTable', 'data'),
    Output('CalendarTable', 'columns'),
    Output('AddProjectCal', 'value'),
    Input('AddProjectCal', 'value'),
    Input('Datepicker', 'date'),
)
def SetDatesCalendar(addProject, start_date):
    con = engine.connect()
    try:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
    except:
        start_date = dt.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    weekday = int(start_date.weekday())
    start = start_date + datetime.timedelta(days=-1 * weekday)
    end = start_date + datetime.timedelta(days=6 - weekday)

    for i in range(0, 7):
        day = (start + datetime.timedelta(days=i)).strftime('%Y-%m-%d')

        df = pd.read_sql \
            (f"""
            SELECT title, timestamp, hours FROM skameyka.main_table m, skameyka.project_table p
            WHERE m.timestamp = '{day}' AND user_id = (SELECT id FROM user_table WHERE fullname like '{flask_login.current_user.name}')
            AND m.project_id = p.id;
        """, con)
        df = df.drop('timestamp', axis=1)
        df.columns = ['НАЗВАНИЕ ПРОЕКТА', WEEKDAYS[i]]

        if i == 0:
            calendar = df
        else:
            calendar = calendar.merge(df, on='НАЗВАНИЕ ПРОЕКТА', how='outer')
    if addProject is not None:
        newdf = pd.DataFrame({'НАЗВАНИЕ ПРОЕКТА': [addProject], 'ПН': [None], 'ВТ': [None], 'СР': [None], 'ЧТ': [None], 'ПТ': [None], 'СБ': [None], 'ВС': [None]})
        calendar = pd.concat([calendar,newdf])
    columns = [{"name": i, "id": i} for i in ['НАЗВАНИЕ ПРОЕКТА'] + WEEKDAYS]
    columns[0]['editable'] = False

    return start, end.strftime('%d.%m.%Y'), calendar.to_dict('records'), columns, None

@appDash.callback(
    Output('popup', 'children'),
    Input('CalendarSave', 'n_clicks'),
    State('popup', 'children'),
    prevent_initial_call=True
)
def SaveCalendar(n_clicks, old):
    con = engine.connect()
    if len(calendar_cache) == 0:
        return old + [
            html.Div([html.Span('😬', className='symbol emoji'), 'Нет изменений'], className='cloud line popup white',hidden=False)]
    try:
        for sql in calendar_cache:

            con.execute(sql)

        for i in range(0, len(calendar_cache)): del calendar_cache[0]
        return old + [html.Div([html.Span('✔', className='symbol'), 'Успешно сохранено'], className='cloud line popup green', hidden=False)]

    except Exception as e:
        e_type, e_val, e_tb = sys.exc_info()
        traceback.print_exception(e_type, e_val, e_tb, file=open('log.txt', 'a'))
        for i in range(0, len(calendar_cache)): del calendar_cache[0]
        return old + [html.Div([html.Span('😧', className='symbol emoji'), 'Возникла ошибка!'], className='cloud line popup orange', hidden=False)]



@appDash.callback(
    Output('popupBox', 'children'),
    Input('popup', 'children'),
    prevent_initial_call=True
)
def SaveCalendar(ch):
    if len(ch) != 0:
        sleep(2.5)
        return html.Div([], id='popup', className='line')
    else:
        dash.no_update()


@appDash.callback(
    Output('pie-chart', 'figure'),
    Output('pie-chart', 'style'),
    Input('CalendarTable', 'data'),
)
def UpdatePie(data):
    global calendar
    calendar = pd.DataFrame(data)
    if calendar.empty:
        style = dict(display='none')
        return dash.no_update, style
    else:
        style = dict(visibility='visible')
        calendar[WEEKDAYS] = calendar[WEEKDAYS].apply(pd.to_numeric)

    # calendar.info()
    colors = ['#393E46', '#00ADB5', '#AAD8D3', '#EEEEEE', '#8ee8e4', '#F3F4ED', '#30475E', '4CA1A3']
    mart = calendar.fillna(0)

    # print(style)
    mart['sum'] = mart['ПН'] + mart['ВТ'] + mart['СР'] + mart['ЧТ'] + mart['ПТ'] + mart['СБ'] + mart['ВС']
    mart = mart[['НАЗВАНИЕ ПРОЕКТА', 'sum']]
    labels = mart['НАЗВАНИЕ ПРОЕКТА'].tolist()
    values = mart['sum'].tolist()
    # print(mart)
    # print(mart.info())
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_traces(automargin=False, selector=dict(type='pie'),
                      marker=dict(colors=colors), textfont_size=12,
                      hoverinfo='label+percent', textinfo='none')
    fig.update_layout(
        font_family="Roboto",
        font_color="black",
        font_size=16,
        margin=dict(l=4, r=12, t=20, b=40),
        height=280,
        width=410,
        legend=dict(font=dict(family="Rubik", size=12, color="black")),
        hoverlabel=dict(
            font_size=14,
            font_family="Rubik",
        )
    )
    return fig, style


@appDash.callback(
    Output('CalendarSave', 'style'),
    [Input('CalendarTable', 'data')],
    [State('CalendarTable', 'data_previous')],
    [State('Datepicker', 'date')],
    prevent_initial_call=True
)
def CalendarChanges(current, previous, start_date):

    if previous is None: return dash.no_update
    total = []
    i = 0
    for project in current:
        old_project = previous[i]
        i += 1
        diff = [[k, project[k]] for k in project if k in old_project and project[k] != old_project[k]]
        if len(diff) != 0:
            if old_project[diff[0][0]] is None: status = 'INS'
            elif project[diff[0][0]] == '0' or project[diff[0][0]] is None: status = 'DEL'
            else: status = 'UPD'
            total.append([project['НАЗВАНИЕ ПРОЕКТА']] + diff[0]+[status])
            break
    UPDATE = total[0]

    user = flask_login.current_user.name

    start_date = dt.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    date = start_date + datetime.timedelta(days=WEEK_NUMBERS[UPDATE[1]])
    date = date.strftime('%Y-%m-%d')

    if UPDATE[3] == 'UPD':
        query = f"""
                UPDATE skameyka.main_table SET hours = {UPDATE[2]} WHERE user_id = 
                (SELECT id FROM skameyka.user_table WHERE fullname like '{user}')
                AND project_id = 
                (SELECT id FROM skameyka.project_table WHERE title like '{UPDATE[0]}')  
                AND timestamp = '{date}'
        """
    elif UPDATE[3] == 'DEL':
        query = f"""
                DELETE FROM skameyka.main_table WHERE user_id = 
                (SELECT id FROM skameyka.user_table WHERE fullname like '{user}')
                AND project_id = 
                (SELECT id FROM skameyka.project_table WHERE title like '{UPDATE[0]}')  
                AND timestamp = '{date}'
        """
    else:
        query = f"""
                INSERT INTO skameyka.main_table (user_id, project_id, timestamp, hours) VALUES 
                (
                    (SELECT id FROM skameyka.user_table WHERE fullname like '{user}'),
                    (SELECT id FROM skameyka.project_table WHERE title like '{UPDATE[0]}'),
                    '{date}', {UPDATE[2]}
                )            
                """
    calendar_cache.append(query)

    return dash.no_update



# @appDash.callback(
#     Output('DialogModal', 'is_open'),
#     Input('EditButton', 'n_clicks'),
#     Input('AddButton', 'n_clicks'),
#     prevent_initial_call=True
# )
# def OpenUserEdit(click1, click2):
#     # global UPDATE_DICT
#     # changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     # if 'AddButton' in changed_id:
#     #     UPDATE_DICT = False
#     # elif 'EditButton' in changed_id:
#     #     UPDATE_DICT = True
#     return True

@appDash.callback(
    Output('DialogModal', 'children'),
    Output('DialogModal', 'is_open'),
    Input("tabs", "value"),
    Input("AdmTable", "derived_virtual_selected_row_ids"),
    Input('EditButton', 'n_clicks'),
    Input('AddButton', 'n_clicks'),
    Input('ModalSubmit', 'n_clicks'),
    Input('ModalDelete', 'n_clicks'),
)
def RenderModal(tab, row, clickE, clickA, clickS, clickD):
    con = engine.connect()
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'EditButton' in changed_id:
        UPDATE_DICT = True
        Open = True
    elif 'AddButton' in changed_id:
        UPDATE_DICT = False
        Open = True
    elif 'ModalSubmit' in changed_id:
        return dash.no_update, False
    elif 'ModalDelete' in changed_id:
        return dash.no_update, False
    else:
        UPDATE_DICT = False
        Open = False

    if row is not None and len(row) != 0 : id = row[0]
    else: id = None

    if tab == 'tab-c':
        if UPDATE_DICT:
            df = pd.read_sql(f'SELECT * FROM skameyka.user_table WHERE id ={id}', con)
            row = df.iloc[0]
            Span = 'ID: '+str(row[0])
            UserName = row['fullname']
            UserLogin = row['username']
            UserPass = row['password']
            UserRole = row['admin']
            UserActual = row['relevant']
            Title = UserName.upper()
        else:
            Title = 'Новый Юзер'.upper()
            Span = ''
            UserName, UserLogin, UserPass, UserRole, UserActual = None,None,None,0,1,
        return \
        [
            dbc.ModalHeader([Title,html.Span(Span,style=dict(color='lightgray',fontFamily='"Noah Regular", monospace',marginLeft=6,fontSize=18))],id='ModalHead'),
            dbc.ModalBody(
                [
                    dcc.Input(id='UserName', placeholder='Имя сотрудника', className='inp', value=UserName),
                    dcc.Input(id='UserLogin', placeholder='Логин', className='inp', value=UserLogin),
                    dcc.Input(id='UserPass', placeholder='Пароль', className='inp', value=UserPass),
                    dbc.Label("Роль", html_for="slider"),
                    dcc.Slider(id="UserRole", min=0, max=1, step=1, value=UserRole, marks={0: 'Юзер', 1: 'Админ'}, ),
                    dcc.Checklist(id='UserActual',className='check',options=[{'label': 'Актуальный', 'value': '1'},],value=f'{UserActual}')
                ], style=dict(paddingLeft=16)
            ),
            dbc.ModalFooter([
                dbc.Button("Удалить", id="ModalDelete", className="button cloud delete", style=dict(visibility='hidden' if not UPDATE_DICT else 'visible') ),
                dbc.Button("Применить", id="ModalSubmit", className="button cloud submit", )]
            ),
        ], Open
    elif tab == 'tab-p':
        stage_marks = {'Концепция': 0, 'ЭП': 1, 'ПД': 2, 'РД': 3}
        if UPDATE_DICT:
            df = pd.read_sql(f'SELECT * FROM skameyka.project_table WHERE id ={id}', con)
            row = df.iloc[0]
            Span = 'ID: ' + str(row[0])
            PrjName = row['title']
            PrjCode = row['code']
            PrjCustomer = row['customer']
            PrjStage = row['stage']
            PrjActual = row['relevant']
            Title = PrjName
        else:
            Title = 'Новый Проект'
            Span = ''
            PrjName, PrjCode, PrjCustomer, PrjStage, PrjActual = None,None,None,'Концепция',None,
        return \
            [
                dbc.ModalHeader([Title, html.Span(Span, style=dict(color='lightgray',fontFamily='"Noah Regular", monospace',marginLeft=6,fontSize=18))],id='ModalHead'),
                dbc.ModalBody(
                    [
                        dcc.Input(id='PrjName', placeholder='Название проекта', className='inp', value=PrjName),
                        dcc.Input(id='PrjCode', placeholder='Шифр', className='inp', value=PrjCode),
                        dcc.Input(id='PrjCustomer', placeholder='Заказчик', className='inp', value=PrjCustomer),
                        dbc.Label("Этап", html_for="slider"),
                        dcc.Slider(id="PrjStage", min=0, max=3, step=1, value=stage_marks[PrjStage], marks={0: 'Концепция', 1: 'ЭП', 2:'ПД', 3:'РД'}, ),
                        dcc.Checklist(id='PrjActual', className='check',
                                      options=[{'label': 'Актуальный', 'value': '1'}, ], value=f'{PrjActual}')
                    ], style=dict(paddingLeft=16)
                ),
                dbc.ModalFooter([
                    dbc.Button("Удалить", id="ModalDelete", className="button cloud delete",  style=dict(visibility='hidden' if not UPDATE_DICT else 'visible')),
                    dbc.Button("Применить", id="ModalSubmit", className="button cloud submit")]
                ),
            ], Open


@appDash.callback(
    Output('popupAdm', 'children'),
    [Input('ModalSubmit', 'n_clicks')],
    [Input('ModalDelete', 'n_clicks')],
    [State('popupAdm', 'children')],
    [State('ModalHead', 'children')],
    [State("tabs", "value")],
    prevent_initial_call=True
)
def UpdateDict(n_clicks1, n_clicks2, old, head, tab):
    con = engine.connect()
    if n_clicks1 is None and n_clicks2 is None: return dash.no_update
    UPDATE = False
    DELETE = False
    CREATE = False
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'ModalSubmit' in changed_id and ('новый юзер' in head[0].lower() or 'новый проект' in head[0].lower()):
        CREATE = True
    elif 'ModalDelete' in changed_id:
        DELETE = True
    elif 'ModalSubmit' in changed_id:
        UPDATE = True
    else: return dash.no_update

    if tab == 'tab-c':
        pass
    elif tab == 'tab-p':
        pass

    return old + [
        html.Div([html.Span('✔', className='symbol'), 'Успешно сохранено'], className='cloud line popup green', hidden=False)]

    # if len(calendar_cache) == 0:
    #     return old + [
    #         html.Div([html.Span('😬', className='symbol emoji'), 'Нет изменений'], className='cloud line popup white',hidden=False)]
    # try:
    #     for sql in calendar_cache:
    #         print(sql)
    #         con.execute(sql)
    #
    #     for i in range(0, len(calendar_cache)): del calendar_cache[0]
    #     return old + [html.Div([html.Span('✔', className='symbol'), 'Успешно сохранено'], className='cloud line popup green', hidden=False)]
    #
    # except Exception as e:
    #     e_type, e_val, e_tb = sys.exc_info()
    #     traceback.print_exception(e_type, e_val, e_tb, file=open('log.txt', 'a'))
    #     for i in range(0, len(calendar_cache)): del calendar_cache[0]
    #     return old + [html.Div([html.Span('😧', className='symbol emoji'), 'Возникла ошибка!'], className='cloud line popup orange', hidden=False)]

