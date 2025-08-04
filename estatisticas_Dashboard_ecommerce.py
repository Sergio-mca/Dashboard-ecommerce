import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Configurações de estilo
sns.set(style="whitegrid")

# 1. Lê o arquivo CSV
df = pd.read_csv('C:\\Users\\SERGIO\\Desktop\\EBAC\\ecommerce_estatistica.csv')

# 2. Mostra informações básicas do DataFrame
print(df.info())
print(df.describe())
print(df.head())

# 3. Histograma - Distribuição dos preços
plt.figure(figsize=(8, 5))
sns.histplot(df['Preço'], kde=True, bins=30)
plt.title('Distribuição dos Preços')
plt.xlabel('Preço')
plt.ylabel('Frequência')
plt.show()

# 4. Gráfico de dispersão - Preço vs Número de Avaliações
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='Preço', y='N_Avaliações', hue='Temporada')
plt.title('Dispersão: Preço x Nº de Avaliações')
plt.xlabel('Preço')
plt.ylabel('Nº de Avaliações')
plt.show()

# 5. Mapa de Calor - Correlação entre variáveis numéricas
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Mapa de Calor das Correlações')
plt.show()

# 6. Gráfico de barras - Média de preço por temporada
plt.figure(figsize=(8, 5))
media_temporada = df.groupby('Temporada')['Preço'].mean().sort_values()
media_temporada.plot(kind='bar', color='skyblue')
plt.title('Preço Médio por Temporada')
plt.xlabel('Temporada')
plt.ylabel('Preço Médio')
plt.xticks(rotation=45)
plt.show()

# 7. Gráfico de pizza - Proporção de produtos por material
plt.figure(figsize=(6, 6))
df['Material'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.title('Distribuição por Material')
plt.ylabel('')
plt.show()

# 8. Gráfico de Densidade - Nota média dos produtos
plt.figure(figsize=(8, 5))
sns.kdeplot(df['Nota'], fill=True)
plt.title('Densidade da Nota dos Produtos')
plt.xlabel('Nota')
plt.ylabel('Densidade')
plt.show()

# 9. Gráfico de Regressão - Preço vs Quantidade Vendida
plt.figure(figsize=(8, 5))
df['Preço'] = pd.to_numeric(df['Preço'], errors='coerce')
df['Qtd_Vendidos'] = pd.to_numeric(df['Qtd_Vendidos'], errors='coerce')
df = df.dropna(subset=['Preço', 'Qtd_Vendidos'])
sns.regplot(data=df, x='Preço', y='Qtd_Vendidos', scatter_kws={'alpha':0.5})
plt.title('Regressão: Preço x Quantidade Vendida')
plt.xlabel('Preço')
plt.ylabel('Qtd Vendidos')
plt.show()

# Tarefa Dashboard ecommerce estatistica

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('C:\\Users\\SERGIO\\Desktop\\EBAC\\ecommerce_estatistica.csv')

lista_genero = df['Gênero'].unique()
options = [{'label': genero, 'value': genero} for genero in lista_genero]

def cria_graficos(selecao_genero):
    filtro_df = df[df['Gênero'].isin(selecao_genero)]

    fig1 = px.bar(
        filtro_df,
        x="Material",
        y="Preço",
        color='Gênero',
        barmode="group",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig1.update_layout(
        title='Preço por Material e Gênero',
        xaxis_title='Material',
        yaxis_title='Preço',
        legend_title='Gênero',
        plot_bgcolor='rgba(222, 255, 253, 1)',
        paper_bgcolor='rgba(186, 245, 241, 1)'
    )

    fig2 = px.scatter_3d(filtro_df, x='Nota', y='Preço', z='Qtd_Vendidos_Cod', color='Gênero')
    fig2.update_layout(
        title='3D: Nota x Preço x Quantidade Vendida',
        scene=dict(
            xaxis_title='Nota',
            yaxis_title='Preço',
            zaxis_title='Qtd Vendidos Cod'
        )
    )

    return fig1, fig2

def cria_app():
    app = Dash(__name__)

    app.layout = html.Div([
        html.H1("Dashboard Interativo - E-commerce"),
        html.Div("Filtre os dados por Gênero para visualizar diferentes padrões."),
        html.Br(),
        html.H2("Preço por Material e Gênero"),
        dcc.Checklist(
            id='id_selecao_genero',
            options=options,
            value=[lista_genero[0]],
        ),
        dcc.Graph(id='id_grafico_barra'),
        dcc.Graph(id='id_grafico_3d')
    ])
    return app

# Executa o app
if __name__ == '__main__':
    app = cria_app()

    @app.callback(
        [
            Output('id_grafico_barra', 'figure'),
            Output('id_grafico_3d', 'figure')
        ],
        [Input('id_selecao_genero', 'value')]
    )
    def atualiza_grafico(selecao_genero):
        fig1, fig2 = cria_graficos(selecao_genero)
        return [fig1, fig2]

    app.run(debug=True, port=8050)