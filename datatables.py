import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from app import usersDF, prjsDF

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
            'font-size': '14px', 'padding-left':'12px'}
style_header={'background-color': '#E1E1E1', 'color': 'black', 'height': '35px','z-index':'5',
              'border': '0px solid white', 'font-family': 'Rubik', 'font-size': '14px'}
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
    }
]
def UsersTable():
    usersDF['ПОСЛЕДНЯЯ АКТИВНОСТЬ'] = usersDF['ПОСЛЕДНЯЯ АКТИВНОСТЬ'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        dash_table.DataTable(
            data = usersDF.to_dict('records'),
            columns=[{"name": i, "id": i} for i in usersDF.columns],
            style_table = style_table,
            style_cell= style_cell,
            style_header=style_header,
            style_as_list_view=True,
            style_data_conditional=style_data_conditional,

        )
    ])
    return content

def ProjectsTable():
    prjsDF['ПОСЛЕДНЕЕ ДЕЙСТВИЕ'] = prjsDF['ПОСЛЕДНЕЕ ДЕЙСТВИЕ'].map(lambda x: str(x).split(' ')[0])
    prjsDF['ШИФР'] = prjsDF['ШИФР'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        dash_table.DataTable(
            data=prjsDF.to_dict('records'),
            columns=[{"name": i, "id": i} for i in prjsDF.columns],
            style_table=style_table,
            style_cell=style_cell,
            style_header=style_header,
            style_as_list_view=True,
            style_data_conditional=style_data_conditional,
        )
    ])
    return content
