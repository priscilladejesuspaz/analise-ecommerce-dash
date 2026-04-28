import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ── Dados ──────────────────────────────────────────────────────────────────────
df = pd.read_csv('ecommerce_estatistica.csv')

# Converter Qtd_Vendidos para numérico
qtd_map = {'+5': 5, '+25': 25, '+50': 50, '+100': 100,
           '+1000': 1000, '+10mil': 10000, '+50mil': 50000}
df['Qtd_Vendidos_Num'] = df['Qtd_Vendidos'].map(qtd_map)

# Padronizar materiais (agrupar variantes de jeans)
df['Material_Clean'] = df['Material'].replace({
    'jeans': 'jean', 'brim 100% algodão': 'algodão',
    'algodão 95%': 'algodão'
})

# Top 10 marcas por qtd de produtos
top_marcas = df['Marca'].value_counts().head(10).index.tolist()
df_top = df[df['Marca'].isin(top_marcas)]

# Paleta
CORES = ['#C0392B', '#E74C3C', '#E8724A', '#F39C12',
         '#F1C40F', '#27AE60', '#2ECC71', '#2980B9',
         '#3498DB', '#8E44AD']
BG    = '#FAFAF9'
CARD  = '#FFFFFF'
TEXT  = '#1A1A1A'
MUTED = '#6B6B6B'

# ── Layout ─────────────────────────────────────────────────────────────────────
app = Dash(__name__, title='Análise E-commerce')

app.layout = html.Div(style={'backgroundColor': BG, 'fontFamily': 'Georgia, serif',
                              'minHeight': '100vh', 'padding': '0'}, children=[

    # Header
    html.Div(style={'backgroundColor': '#1A1A1A', 'padding': '28px 40px',
                    'borderBottom': '3px solid #C0392B'}, children=[
        html.H1('Análise de E-commerce', style={'color': '#FFFFFF', 'margin': 0,
                'fontSize': '26px', 'fontWeight': 'normal', 'letterSpacing': '1px'}),
        html.P('Moda e vestuário · 295 produtos · Mercado Livre',
               style={'color': '#999', 'margin': '4px 0 0', 'fontSize': '13px',
                      'fontFamily': 'Helvetica, sans-serif'})
    ]),

    # KPIs
    html.Div(style={'display': 'flex', 'gap': '16px', 'padding': '28px 40px 0',
                    'flexWrap': 'wrap'}, children=[
        kpi('295', 'Produtos analisados', '#C0392B'),
        kpi(f"{df['Nota'].mean():.2f}", 'Nota média', '#E74C3C'),
        kpi(f"R$ {df['Preço'].mean():.0f}", 'Preço médio', '#2980B9'),
        kpi(f"{df['Desconto'].mean():.1f}%", 'Desconto médio', '#27AE60'),
        kpi(str(df['Marca'].nunique()), 'Marcas únicas', '#8E44AD'),
    ]),

    # Filtros
    html.Div(style={'padding': '24px 40px 0', 'display': 'flex', 'gap': '24px',
                    'flexWrap': 'wrap', 'alignItems': 'flex-end'}, children=[
        html.Div([
            html.Label('Gênero', style={'fontSize': '12px', 'color': MUTED,
                       'fontFamily': 'Helvetica, sans-serif', 'display': 'block',
                       'marginBottom': '6px'}),
            dcc.Dropdown(
                id='filtro-genero',
                options=[{'label': g, 'value': g}
                         for g in sorted(df['Gênero'].unique())],
                placeholder='Todos os gêneros',
                clearable=True,
                style={'width': '220px', 'fontFamily': 'Helvetica, sans-serif',
                       'fontSize': '13px'}
            )
        ]),
        html.Div([
            html.Label('Temporada', style={'fontSize': '12px', 'color': MUTED,
                       'fontFamily': 'Helvetica, sans-serif', 'display': 'block',
                       'marginBottom': '6px'}),
            dcc.Dropdown(
                id='filtro-temporada',
                options=[{'label': t, 'value': t}
                         for t in sorted(df['Temporada'].unique())],
                placeholder='Todas as temporadas',
                clearable=True,
                style={'width': '260px', 'fontFamily': 'Helvetica, sans-serif',
                       'fontSize': '13px'}
            )
        ]),
    ]),

    # Gráficos linha 1
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
                    'gap': '20px', 'padding': '24px 40px 0'}, children=[
        card_grafico('grafico-nota-marca',    'Nota média por marca (top 10)'),
        card_grafico('grafico-preco-genero',  'Distribuição de preço por gênero'),
    ]),

    # Gráficos linha 2
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
                    'gap': '20px', 'padding': '20px 40px 0'}, children=[
        card_grafico('grafico-material',      'Produtos por material'),
        card_grafico('grafico-desconto',      'Desconto × Nota (por gênero)'),
    ]),

    # Gráficos linha 3
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr',
                    'gap': '20px', 'padding': '20px 40px 0'}, children=[
        card_grafico('grafico-vendidos',      'Quantidade vendida por faixa'),
        card_grafico('grafico-temporada',     'Produtos por temporada'),
    ]),

    # Gráfico largo
    html.Div(style={'padding': '20px 40px 40px'}, children=[
        html.Div(style=card_style(), children=[
            html.P('Preço × Nota por material', style=titulo_style()),
            dcc.Graph(id='grafico-scatter', config={'displayModeBar': False})
        ])
    ])
])


# ── Helpers ────────────────────────────────────────────────────────────────────
def kpi(valor, label, cor):
    return html.Div(style={
        'backgroundColor': CARD, 'border': f'1px solid #E8E8E8',
        'borderTop': f'3px solid {cor}', 'borderRadius': '4px',
        'padding': '16px 20px', 'minWidth': '140px', 'flex': '1'
    }, children=[
        html.P(label, style={'fontSize': '11px', 'color': MUTED, 'margin': '0 0 6px',
               'fontFamily': 'Helvetica, sans-serif', 'textTransform': 'uppercase',
               'letterSpacing': '0.5px'}),
        html.P(valor, style={'fontSize': '24px', 'color': TEXT, 'margin': 0,
               'fontWeight': 'normal'})
    ])

def card_style():
    return {'backgroundColor': CARD, 'border': '1px solid #E8E8E8',
            'borderRadius': '4px', 'padding': '20px'}

def titulo_style():
    return {'fontSize': '13px', 'color': MUTED, 'margin': '0 0 12px',
            'fontFamily': 'Helvetica, sans-serif', 'textTransform': 'uppercase',
            'letterSpacing': '0.5px'}

def card_grafico(graph_id, titulo):
    return html.Div(style=card_style(), children=[
        html.P(titulo, style=titulo_style()),
        dcc.Graph(id=graph_id, config={'displayModeBar': False})
    ])

def layout_base():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Helvetica, sans-serif', color=TEXT, size=12),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=True,
        xaxis=dict(showgrid=False, showline=True, linecolor='#E8E8E8'),
        yaxis=dict(showgrid=True, gridcolor='#F0F0F0', showline=False)
    )


# ── Callbacks ──────────────────────────────────────────────────────────────────
def filtrar(df, genero, temporada):
    d = df.copy()
    if genero:
        d = d[d['Gênero'] == genero]
    if temporada:
        d = d[d['Temporada'] == temporada]
    return d


@app.callback(
    Output('grafico-nota-marca', 'figure'),
    Output('grafico-preco-genero', 'figure'),
    Output('grafico-material', 'figure'),
    Output('grafico-desconto', 'figure'),
    Output('grafico-vendidos', 'figure'),
    Output('grafico-temporada', 'figure'),
    Output('grafico-scatter', 'figure'),
    Input('filtro-genero', 'value'),
    Input('filtro-temporada', 'value'),
)
def atualizar(genero, temporada):
    d = filtrar(df, genero, temporada)

    # 1. Nota média por marca (top 10)
    top = d['Marca'].value_counts().head(10).index
    d1  = d[d['Marca'].isin(top)].groupby('Marca')['Nota'].mean().sort_values()
    fig1 = go.Figure(go.Bar(
        x=d1.values, y=d1.index, orientation='h',
        marker_color=CORES[:len(d1)], text=d1.round(2).values,
        textposition='outside'
    ))
    fig1.update_layout(**layout_base())

    # 2. Box plot preço por gênero
    generos_ok = ['Masculino', 'Feminino', 'Sem gênero', 'Meninos', 'Meninas']
    d2 = d[d['Gênero'].isin(generos_ok)]
    fig2 = px.box(d2, x='Gênero', y='Preço', color='Gênero',
                  color_discrete_sequence=CORES)
    fig2.update_layout(**layout_base())
    fig2.update_layout(showlegend=False)

    # 3. Material — barras
    mat = d['Material_Clean'].value_counts().head(8)
    fig3 = go.Figure(go.Bar(
        x=mat.values, y=mat.index, orientation='h',
        marker_color='#C0392B', text=mat.values, textposition='outside'
    ))
    fig3.update_layout(**layout_base())

    # 4. Scatter desconto × nota
    fig4 = px.scatter(d, x='Desconto', y='Nota', color='Gênero',
                      color_discrete_sequence=CORES, opacity=0.7,
                      trendline='ols')
    fig4.update_layout(**layout_base())

    # 5. Qtd vendidos por faixa
    vendidos = d['Qtd_Vendidos'].value_counts().reindex(
        ['+5', '+25', '+50', '+100', '+1000', '+10mil', '+50mil'], fill_value=0)
    fig5 = go.Figure(go.Bar(
        x=vendidos.index, y=vendidos.values,
        marker_color='#2980B9', text=vendidos.values, textposition='outside'
    ))
    fig5.update_layout(**layout_base())

    # 6. Temporada — pizza
    temp_map = {
        'primavera/verão': 'Primavera/Verão',
        'outono/inverno': 'Outono/Inverno',
        'não definido': 'Não definido',
        'primavera-verão outono-inverno': 'Todas',
        'primavera-verão - outono-inverno': 'Todas',
        'primavera/verão/outono/inverno': 'Todas',
        '2021': 'Não definido'
    }
    d['Temporada_Clean'] = d['Temporada'].map(temp_map).fillna(d['Temporada'])
    temp = d['Temporada_Clean'].value_counts()
    fig6 = go.Figure(go.Pie(
        labels=temp.index, values=temp.values,
        marker_colors=CORES, hole=0.4,
        textinfo='label+percent'
    ))
    fig6.update_layout(**layout_base())
    fig6.update_layout(showlegend=False)

    # 7. Scatter preço × nota por material
    mats_top = d['Material_Clean'].value_counts().head(6).index
    d7 = d[d['Material_Clean'].isin(mats_top)]
    fig7 = px.scatter(d7, x='Preço', y='Nota', color='Material_Clean',
                      color_discrete_sequence=CORES, opacity=0.75,
                      labels={'Material_Clean': 'Material'},
                      hover_data=['Marca', 'Desconto'])
    fig7.update_layout(**layout_base())
    fig7.update_layout(height=380)

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7


if __name__ == '__main__':
    app.run(debug=True)
