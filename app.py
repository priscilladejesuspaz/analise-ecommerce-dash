import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv('ecommerce_estatistica.csv')

app = Dash(__name__)

app.layout = html.Div([
    
    html.H1("Análise de E-commerce", style={'textAlign': 'center'}),
    
    dcc.Dropdown(
        id='filtro-genero',
        options=[{'label': g, 'value': g} for g in df['Gênero'].unique()],
        placeholder='Selecione o gênero',
        style={'width': '300px'}
    ),

    dcc.Graph(id='grafico-nota'),
    dcc.Graph(id='grafico-preco'),
    dcc.Graph(id='grafico-material')
])

@app.callback(
    Output('grafico-nota', 'figure'),
    Output('grafico-preco', 'figure'),
    Output('grafico-material', 'figure'),
    Input('filtro-genero', 'value')
)
def atualizar(genero):
    
    if genero:
        dff = df[df['Gênero'] == genero]
    else:
        dff = df

    nota = dff.groupby('Marca')['Nota'].mean().reset_index()
    fig1 = px.bar(nota, x='Marca', y='Nota', title='Nota média por marca')

    fig2 = px.box(dff, x='Gênero', y='Preço', title='Distribuição de preço')

    material = dff['Material'].value_counts().reset_index()
    material.columns = ['Material', 'Quantidade']
    fig3 = px.bar(material, x='Material', y='Quantidade',
                  title='Produtos por material')

    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run(debug=True)
