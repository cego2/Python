import streamlit as st
import pandas as pd
import plotly_express as px
from statsmodels.sandbox.regression.try_treewalker import data2
from streamlit import title


def main():
    #Carregando os dados
    data = pd.read_excel('Base.xlsx', sheet_name='Base')
    titulo = 'Dashboard de Vendas'
    st.set_page_config(page_title=titulo, layout='wide')
    st.title(titulo)

    #Criar filtros
    anos = data['Ano'].unique()
    paises = data['País'].unique()

    filtro_ano = st.sidebar.selectbox('Selecione o Ano', options=['Todos'] + sorted(anos), index=0)
    filtro_pais = st.sidebar.selectbox('Selecione o País', options=['Todos'] + sorted(paises), index=0)

    #Criandno Filtro controlador dos gráficos
    data_filtrada = data
    if filtro_ano != 'Todos':
        data_filtrada = data_filtrada[data_filtrada['Ano'] == filtro_ano]
    if filtro_pais != 'Todos':
        data_filtrada = data_filtrada[data_filtrada['País'] == filtro_pais]

    #Grafico 01
    grafico_lucrosegmento = px.bar(
        data_filtrada.groupby('Segmento')['Lucro'].sum().reset_index(),
        x='Segmento', y='Lucro',
        title='Lucro por Segmento',
        color='Segmento',
        text_auto=True
    )
    grafico_lucrosegmento.update_layout(showlegend=False)
    # Formatar os valores como moeda (Real - R$)
    grafico_lucrosegmento.update_traces(
        texttemplate="R$ %{y:,.2f}",  # Formata os valores como moeda com duas casas decimais
        textposition="outside"  # Exibe os valores acima das barras
    )
    # Formatar o eixo Y para exibir valores monetários corretamente
    grafico_lucrosegmento.update_layout(
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=","
    )

    #Grafico 02
    grafico_vendas_tempo = px.line(
        data_filtrada.groupby(['Data'])['Vendas Brutas'].sum().reset_index(),
        x='Data', y='Vendas Brutas',
        title='Vendas Brutas ao Longo do Tempo',
        markers=True
    )
    #Grafico 03
    grafico_produtos = px.pie(
        data_filtrada.groupby('Produto')['Unidades Vendidas'].sum().reset_index(),
        values='Unidades Vendidas', names='Produto',
        title='Distribuição de Produtos Vendidos',
    )

    #Grafico 04
    custo_lucro_data = data_filtrada.groupby(['Segmento'])[['COGS', 'Lucro']].sum().reset_index().melt(
        id_vars='Segmento', value_vars=['COGS', 'Lucro'])
    custo_lucro_data['value_formatado'] = custo_lucro_data['value'].apply(lambda x: f'R$ {x:,.2f}')

    grafico_custo_lucro = px.bar(
        custo_lucro_data,
        x='Segmento', y='value',
        title='Relação entre Custo e Lucro',
        color='variable',
        barmode='group',
        text='value_formatado'
    )

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col1.plotly_chart(grafico_lucrosegmento, use_container_width=True)
    col2.plotly_chart(grafico_vendas_tempo, use_container_width=True)
    col3.plotly_chart(grafico_produtos, use_container_width=True)
    col4.plotly_chart(grafico_custo_lucro, use_container_width=True)

main()