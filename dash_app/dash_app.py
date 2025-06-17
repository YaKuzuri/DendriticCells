from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import os
import requests
import json

MAIN_HOST_DJANGO = os.environ.get('MAIN_HOST_DJANGO')
HTTP_TYPE = os.environ.get('HTTP_TYPE')

def get_response_check(url_part, info_name, get=True, post_json=None):
    url = HTTP_TYPE + '://' + MAIN_HOST_DJANGO + url_part
    print(url)
    if get:
        response = requests.get(url)
    else:
        response = requests.post(url, json=post_json)
    if response.status_code == 200:
        json_data = json.loads(response.content)
        df = pd.DataFrame.from_dict(json_data[info_name])
        status = 'Данные загруженны'
        cr = 'success'
        error = False
    else:
        status = f'Ошибка загрузки данных: {response.status_code}. Перезагрузите страницу.'
        df = pd.DataFrame()
        cr = 'danger'
        error = True

    return df, status, cr, error

# response = requests.get('http://127.0.0.1:8000/api/get_all')
# json_data = json.loads(response.content)
# df = pd.DataFrame.from_dict(json_data['patients'])
df, status, cr, error = get_response_check('/api/get_all', 'patients', get=True, post_json=None)
print(df)
print(df.columns)
print(status)

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    html.A(href='http://127.0.0.1:8000', children='На главную страницу', style={'textAlign':'center'}),
    dash_table.DataTable(
        id='table',
        columns=[
            {
                "name": i,
                "id": i,
                "deletable": True,
                "selectable": True} for i in df.columns
        ],
        # hidden_columns=[i for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
        export_format='xlsx',

        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        filter_options={
            'placeholder_text': 'Фильтр...',
        },
        style_table={'overflowX': 'auto'},
    ),
    dcc.Graph(id='graph-content')
]

# @callback(
#     Output('graph-content', 'figure'),
#     Input('dropdown-selection', 'value')
# )
# def update_graph(value):
#     dff = df[df.country==value]
#     return px.line(dff, x='year', y='pop')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
