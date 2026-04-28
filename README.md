# Análise de E-commerce - Dashboard Interativo com Dash

## Sobre o projeto

Aplicação web interativa desenvolvida com **Dash (Plotly)** para análise de produtos de moda e vestuário do Mercado Livre.

O usuário final consegue explorar os dados sem precisar interagir com Python - basta acessar o link da aplicação.

## Dashboard

A aplicação contém **7 visualizações interativas** com filtros por gênero e temporada:

| Gráfico | Insight |
|---------|---------|
| Nota média por marca (top 10) | Quais marcas têm melhor avaliação |
| Distribuição de preço por gênero | Comparativo de faixa de preço |
| Produtos por material | Materiais mais comuns no catálogo |
| Desconto × Nota | Relação entre desconto e avaliação |
| Quantidade vendida por faixa | Perfil de volume de vendas |
| Produtos por temporada | Sazonalidade do catálogo |
| Preço × Nota por material | Custo-benefício por tipo de material |

## Ferramentas

- Python 3
- Dash 2.17
- Plotly 5
- pandas

## Como rodar localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
python app.py
```

Abra o navegador em `http://127.0.0.1:8050`

## Estrutura

```
analise-ecommerce-dash/
├── app.py                      → aplicação Dash principal
├── ecommerce_estatistica.csv   → dataset de produtos
├── requirements.txt            → dependências
└── README.md
```

## Dados

Dataset de produtos de moda e vestuário com 295 registros e 24 variáveis, incluindo nota, preço, desconto, marca, material, gênero, temporada e quantidade vendida.

## Aprendizados

- Estrutura de uma aplicação Dash (layout + callbacks)
- Criação de gráficos interativos com Plotly
- Filtros reativos com `Input` e `Output`
- Boas práticas de visualização de dados para usuário final
