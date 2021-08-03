import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import appDash
import dash
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
    usersDF['ПОСЛЕДНЯЯ АКТИВНОСТЬ'] = usersDF['ПОСЛЕДНЯЯ АКТИВНОСТЬ'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        dash_table.DataTable(
            data = usersDF.to_dict('records'),
            columns=[{"name": i, "id": i} for i in usersDF.columns],
            id='UsersTable',
            style_table = style_table,
            style_cell= style_cell,
            style_header=style_header,

            style_as_list_view=True,
            style_data_conditional=style_data_conditional,
            row_selectable='single',
            # derived_virtual_selected_rows=[]
        )
    ])
    return content

def ProjectsTable():
    prjsDF['ПОСЛЕДНЕЕ ДЕЙСТВИЕ'] = prjsDF['ПОСЛЕДНЕЕ ДЕЙСТВИЕ'].map(lambda x: str(x).split(' ')[0])
    prjsDF['ШИФР'] = prjsDF['ШИФР'].map(lambda x: str(x).split(' ')[0])
    content = html.Div([
        dash_table.DataTable(
            data=prjsDF.to_dict('records'),
            id='ProjectsTable',
            columns=[{"name": i, "id": i} for i in prjsDF.columns],
            style_table=style_table,
            style_cell=style_cell,
            style_header=style_header,
            style_as_list_view=True,
            style_data_conditional=style_data_conditional,
            # row_selectable='single',
        )
    ])
    return content

@appDash.callback(
    Output("UsersTable", "style_data_conditional"),
    Input("UsersTable", "active_cell"),
)
def style_selected_rows(sel_rows):

    if sel_rows is None:
        return dash.no_update
    val = [
        {"if": {"filter_query": "{{id}} ={}".format(sel_rows['row_id'])}, "backgroundColor": "rgba(0, 116, 217, 0.3)",}
        for i in sel_rows
    ]
    print(val)
    return style_data_conditional+val
    # return [sel_rows['row_id']]

# @appDash.callback(
#     Output("ProjectsTable", "style_data_conditional"),
#     Input("ProjectsTable", "derived_virtual_selected_row_ids"),
# )
# def style_selected_rows(sel_rows):
#     print(sel_rows)
#     if sel_rows is None:
#         return dash.no_update
#     val = [
#         {"if": {"filter_query": "{{id}} ={}".format(i)}, "backgroundColor": "rgba(0, 116, 217, 0.3)",}
#         for i in sel_rows
#     ]
#     print(val)
#     return style_data_conditional+val
#
# @appDash.callback(
#     Output("ProjectsTable", "derived_virtual_selected_row_ids"),
#     Input("ProjectsTable", "active_cell"),
# )
# def select_cell(cell):
#     print(cell)
#     if cell is None:
#         return dash.no_update
#     return [cell['row_id']]
#
# @appDash.callback(
#     Output("UsersTable", "derived_virtual_selected_row_ids"),
#     Input("UsersTable", "active_cell"),
# )
# def select_cell(cell):
#     print(cell)
#     if cell is None:
#         return dash.no_update
#     return [cell['row_id']]