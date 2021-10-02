import pandas as pd
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import appDash, engine
import dash
from sqlalchemy import create_engine
# engine = create_engine('clickhouse://10.200.2.113/recengine')


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
                }
style_cell={'font-family': 'Rubik', 'text-align': 'left', 'width':'auto',
            'border': '3px solid white', 'background-color': '#f7f7f7',
            'font-size': '14px', 'padding-left':'12px','cursor':'pointer'}
style_header={'background-color': '#E1E1E1', 'color': 'black', 'height': '35px','z-index':'5',
              'border': '0px solid white', 'font-family': 'Rubik', 'font-size': '14px','cursor':'default'}
style_data_conditional=[
    {
        'if': {
            'filter_query': '{СТАТУС} eq "Актуальный"',
            'column_id': 'СТАТУС'
        },
        # 'color': '#25c193'
        'color': '#25C193'
    },
    {
        'if': {
            'filter_query': '{СТАТУС} eq "Не актуальный"',
            'column_id': 'СТАТУС'
        },
        'color': 'silver'
    },
    {
        "if": {"state": "selected"},  # 'active' | 'selected'
        "backgroundColor": "rgba(0, 116, 217, 0.3)",
        'border': '3px solid white',
    },
]

def UsersTable():
    # usersDF['ПОСЛЕДНЯЯ АКТИВНОСТЬ'] = usersDF['ПОСЛЕДНЯЯ АКТИВНОСТЬ'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        dash_table.DataTable(

            # columns=[{"name": i, "id": i} for i in usersDF.columns],
            id='AdmTable',
            style_table =    style_table,
            style_cell= style_cell,
            style_header=style_header,
            fixed_rows={'headers': True, 'data': 0},
            style_as_list_view=True,
            style_data_conditional=style_data_conditional,
            # row_selectable='single',
            # derived_virtual_selected_rows=[]
        )
    ])
    return content

def ProjectsTable():
    # prjsDF['ПОСЛЕДНЕЕ ДЕЙСТВИЕ'] = prjsDF['ПОСЛЕДНЕЕ ДЕЙСТВИЕ'].map(lambda x: str(x).split(' ')[0])
    # prjsDF['ШИФР'] = prjsDF['ШИФР'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        dash_table.DataTable(

            id='AdmTable',
            # columns=[{"name": i, "id": i} for i in prjsDF.columns],
            style_table=style_table,
            style_cell=style_cell,
            style_header=style_header,
            fixed_rows={'headers': True, 'data': 0},
            style_as_list_view=True,
            style_data_conditional=style_data_conditional,
            # row_selectable='single',
        )
    ])
    return content


@appDash.callback(
    Output("AdmTable", "data"),
    Output("AdmTable", "columns"),
    Input("tabs", "value"),
)
def AdmTableContent(tab):
    con = engine.connect()
    if tab == 'tab-c':
        df = pd.read_sql("SELECT id, fullname, admin, relevant  FROM skameyka.user_table", con)
        df.columns = ['id','ИМЯ', 'АДМИН', 'СТАТУС']
        df['АДМИН'] = df['АДМИН'].map(lambda x: 'Да' if x == 1 else 'Нет')
        df['СТАТУС'] = df['СТАТУС'].map(lambda x: 'Актуальный' if x == 1 else 'Не актуальный')
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]
    elif tab == 'tab-p':
        df = pd.read_sql("SELECT id, title, stage, code, customer, relevant  FROM skameyka.project_table", con)
        df.columns = ['id', 'НАЗВАНИЕ', 'ЭТАП', 'ШИФР', 'ЗАКАЗЧИК', 'СТАТУС']
        df['СТАТУС'] = df['СТАТУС'].map(lambda x: 'Актуальный' if x == 1 else 'Не актуальный')
        return df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]


@appDash.callback(
    Output("AdmTable", "style_data_conditional"),
    Input("AdmTable", "active_cell"),
)
def style_selected_rows(sel_rows):
    if sel_rows is None:
        return dash.no_update
    val = [
        {"if": {"filter_query": "{{id}} ={}".format(sel_rows['row_id'])}, "backgroundColor": "rgba(0, 116, 217, 0.3)",}
        for i in sel_rows
    ]
    return style_data_conditional+val
    # return [sel_rows['row_id']]

@appDash.callback(
    Output("AdmTable", "derived_virtual_selected_row_ids"),
    Input("AdmTable", "active_cell"),
)
def select_cell(cell):
    if cell is None:
        return dash.no_update
    print([cell['row_id']])
    return [cell['row_id']]

@appDash.callback(
    Output("EditButton", "style"),
    Input("AdmTable", "active_cell"),
    prevent_initial_call = True
)
def show_button(cell1):
    if cell1 is None:
        return {'display':'none'}
    return {'display':'inline-block'}

