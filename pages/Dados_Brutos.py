import pandas as pd
import streamlit as st
import requests

st.title('Dados Brutos')

url                  = 'https://labdados.com/produtos'
response             = requests.get(url)
df                   = pd.DataFrame.from_dict(response.json())
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

with st.expander('Colunas'):
  colunas = st.multiselect('Selecione as colunas', list(df.columns), list(df.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do Produto'):
  produtos = st.multiselect('Selecione os Produtos', df['Produto'].unique(), df['Produto'].unique())
with st.sidebar.expander('Preço do Produto'):
  preco = st.slider('Selecione o Preço', 0, 5000, (0, 5000))
with st.sidebar.expander('Data da Compra'):
  data_compra = st.date_input('Selecione a Data', (df['Data da Compra'].min(), df['Data da Compra'].max()))
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos', df['Produto'].unique(), df['Produto'].unique())
with st.sidebar.expander('Categoria do produto'):
    categoria = st.multiselect('Selecione as categorias', df['Categoria do Produto'].unique(), df['Categoria do Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço', 0, 5000, (0, 5000))
with st.sidebar.expander('Frete da venda'):
    frete = st.slider('Frete', 0,250, (0, 250))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', (df['Data da Compra'].min(), df['Data da Compra'].max()))
with st.sidebar.expander('Vendedor'):
    vendedores = st.multiselect('Selecione os vendedores', df['Vendedor'].unique(), df['Vendedor'].unique())
with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local da compra', df['Local da compra'].unique(), df['Local da compra'].unique())
with st.sidebar.expander('Avaliação da compra'):
    avaliacao = st.slider('Selecione a avaliação da compra',1, 5, value = (1, 5))
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',df['Tipo de pagamento'].unique(), df['Tipo de pagamento'].unique())
with st.sidebar.expander('Quantidade de parcelas'):
    qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1, 24))
st.dataframe(df, column_config={
  'Preço': st.column_config.NumberColumn(format='%.2f 🪙'),
  'Frete': st.column_config.NumberColumn(format='%.2f 🚚')
})
