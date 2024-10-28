from dash import Dash, dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px

# Inicialize a aplicação Dash
app = Dash(__name__)

# Exemplo de dados 
data = pd.read_excel('C:/Users/elome/OneDrive/Desktop/estudos/PASTA PROJETO/venv/Vendas.xlsx')
df = pd.DataFrame(data)

# Figuras
fig_pie = px.pie(df, values='Quantidade', names='Produto', title='Quantidade vendida por produto')
fig_hist = px.histogram(df, x='ID Loja', y='Quantidade', histfunc='sum', title='Quantidade de Produtos Vendidos por Loja')
fig_line = px.line(df, x='Data', y='Valor Final', title='Faturamento por Mês', markers=True)


# Layout da aplicação
app.layout = html.Div([
    # Filtros interativos
    html.Div([
        html.Label("ID Loja:"),
        dcc.Dropdown(
            id='idloja-filter',
            options=[{'label': loja, 'value': loja} for loja in df['ID Loja'].unique()],
            placeholder="Selecione o ID da Loja",
            multi=True
        ),
        html.Label("Produto:"),
        dcc.Dropdown(
            id='produto-filter',
            options=[{'label': produto, 'value': produto} for produto in df['Produto'].unique()],
            placeholder="Selecione o Produto",
            multi=True
        ),
        # Gráficos
        dcc.Graph(figure=fig_pie),  # Gráfico de pizza
        dcc.Graph(figure=fig_hist),  # Histograma
        dcc.Graph(figure=fig_line),  # Gráfico de linha
    ], style={'padding': 10}),

    # Tabela interativa
    dash_table.DataTable(
        id='project-table',
        columns=[
            {'name': 'Código Venda', 'id': 'Código Venda'},  # Texto ou número, sem formatação específica
            {'name': 'Data', 'id': 'Data', 'type': 'datetime'},  # Formato de data
            {'name': 'ID Loja', 'id': 'ID Loja'},  # Texto ou número, sem formatação específica
            {'name': 'Produto', 'id': 'Produto'},  # Texto, sem formatação específica
            {'name': 'Quantidade', 'id': 'Quantidade', 'type': 'numeric', 'format': {'specifier': ',.0f'}},  # Inteiro sem casas decimais
            {'name': 'Valor Unitário', 'id': 'Valor Unitário', 'type': 'numeric', 'format': {'specifier': '$,.2f'}},  # Valor em formato de moeda
            {'name': 'Valor Final', 'id': 'Valor Final', 'type': 'numeric', 'format': {'specifier': '$,.2f'}}  # Valor em formato de moeda
        ],
        data=df.to_dict('records'),
        style_cell={'textAlign': 'center'},
        style_data_conditional=[
            {
                'if': {'column_id': 'Completion'},
                'backgroundColor': 'lightgrey',
                'padding': '0 5px'
            }
        ],
        style_table={'overflowX': 'auto'}
    )
])



# Callback para atualizar a tabela com base nos filtros
@app.callback(
    Output('project-table', 'data'),
    [Input('idloja-filter', 'value'),
     Input('produto-filter', 'value')]
)
def update_table(selected_idloja, selected_produto):
    # Filtro básico para ID Loja e Produto
    filtered_df = df
    if selected_idloja:
        filtered_df = filtered_df[filtered_df['ID Loja'].isin(selected_idloja)]
    if selected_produto:
        filtered_df = filtered_df[filtered_df['Produto'].isin(selected_produto)]
    return filtered_df.to_dict('records')

# Execute o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
