import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import plotly.express as px

# Cargar bases de datos
url_coacel = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3uqYngG2O1K07T4FMip3zvB1K1hLfKnFyxwEizn9R58-NQsxncOAKi2bWtH_Y81AqC8SazM1dqfSB/pub?gid=0&single=true&output=csv"
url_convivir = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS3uqYngG2O1K07T4FMip3zvB1K1hLfKnFyxwEizn9R58-NQsxncOAKi2bWtH_Y81AqC8SazM1dqfSB/pub?gid=1009429221&single=true&output=csv"

df_coacel = pd.read_csv(url_coacel)
df_convivir = pd.read_csv(url_convivir)

# Unir bases de datos
df = pd.concat([df_coacel, df_convivir])

# Inicializar la aplicación
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1('Búsqueda de Productos Sin Gluten'),
    html.Div([
        html.Div([
            html.Label('Seleccionar Base de Datos:'),
            dcc.Dropdown(
                id='base-de-datos',
                options=[
                    {'label': 'Coacel', 'value': 'coacel'},
                    {'label': 'Convivir', 'value': 'convivir'},
                    {'label': 'Ambas', 'value': 'ambas'}
                ],
                value='ambas'
            )
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Buscar Producto:'),
            dcc.Input(id='buscar-producto', type='text', placeholder='Buscar por palabra')
        ], style={'width': '49%', 'display': 'inline-block'}),
    ]),
    html.Div([
        html.Div([
            html.Label('Empresa:'),
            dcc.Dropdown(id='empresa')
        ], style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Categoría:'),
            dcc.Dropdown(id='categoria')
        ], style={'width': '49%', 'display': 'inline-block'}),
    ]),
    html.Div(id='tabla-productos'),
    html.Div(id='grafico-distribucion')
])

# Callback para actualizar empresas y categorías
@app.callback(
    [Output('empresa', 'options'),
     Output('categoria', 'options')],
    [Input('base-de-datos', 'value')]
)
def actualizar_opciones(base_de_datos):
    if base_de_datos == 'coacel':
        df_filtrado = df_coacel
    elif base_de_datos == 'convivir':
        df_filtrado = df_convivir
    else:
        df_filtrado = df
    
    empresas = [{'label': e, 'value': e} for e in df_filtrado['Empresa'].unique()]
    categorias = [{'label': c, 'value': c} for c in df_filtrado['Categoría'].unique()]
    
    return empresas, categorias

# Callback para mostrar tabla de productos
@app.callback(
    Output('tabla-productos', 'children'),
    [Input('base-de-datos', 'value'),
     Input('buscar-producto', 'value'),
     Input('empresa', 'value'),
     Input('categoria', 'value')]
)
def mostrar_productos(base_de_datos, buscar_producto, empresa, categoria):
    if base_de_datos == 'coacel':
        df_filtrado = df_coacel
    elif base_de_datos == 'convivir':
        df_filtrado = df_convivir
    else:
        df_filtrado = df
    
    if buscar_producto:
        df_filtrado = df_filtrado[df_filtrado['Producto'].str.contains(buscar_producto, case=False)]
    
    if empresa:
        df_filtrado = df_filtrado[df_filtrado['Empresa'] == empresa]
    
    if categoria:
        df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria]
    
    return dash_table.DataTable(df_filtrado.to_dict('records'), [{"name": i, "id": i} for i in df_filtrado.columns])

# Callback para mostrar gráfico de distribución
@app.callback(
    Output('grafico-distribucion', 'children'),
    [Input('base-de-datos', 'value'),
     Input('buscar-producto', 'value'),
     Input('empresa', 'value'),
     Input('categoria', 'value')]
)
def mostrar_grafico(base_de_datos, buscar_producto, empresa, categoria):
    if base_de_datos == 'coacel':
        df_filtrado = df_coacel
    elif base_de_datos == 'convivir':
        df_filtrado = df_convivir
    else:
        df_filtrado = df
    
    if buscar_producto:
        df_filtrado = df_filtrado[df_filtrado['Producto'].str.contains(buscar_producto, case=False)]
    
    if empresa:
        df_filtrado = df_filtrado[df_filtrado['Empresa'] == empresa]
    
    if categoria:
        df_filtrado = df_filtrado[df_filtrado['Categoría'] == categoria]
    
    if buscar_producto:
        fig = px.bar(df_filtrado['Empresa'].value_counts(), title='Distribución de Marcas')
    elif empresa:
        fig = px.bar(df_filtrado['Categoría'].value_counts(), title='Distribución de Categorías')
    else:
        fig = px.bar(df_filtrado['Categoría'].value_counts(), title='Distribución de Categorías')
    
    return dcc.Graph(figure=fig)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
