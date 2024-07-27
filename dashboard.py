import pandas as pd
import streamlit as st
import requests
import plotly.express as px

def format_number(value):
  if value >= 1000000000:
    value = f'{(value / 1000000000):.2f}B'
  elif value >= 1000000:
    value = f'{(value / 1000000):.2f}M'
  elif value >= 1000:
    value = f'{(value / 1000):.2f}K'
  return value

st.set_page_config(layout='wide', page_title='Dashboard de Vendas', page_icon=':shopping_trolley:')
st.title('Dashboard de Vendas :shopping_trolley:')


url      = 'https://labdados.com/produtos'
response = requests.get(url)
df       = pd.DataFrame.from_dict(response.json())

df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')


## Map Income per State ##
receita_estados     = df.groupby('Local da compra')['Preço'].sum()
receita_estados     = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)
fig_receita_estados = px.bar(receita_estados.head(),
                            x='Local da compra', y='Preço', text_auto=True, title='Top Estados por Receita')
fig_map             = px.scatter_geo(receita_estados,
                                    lat='lat', lon='lon', scope='south america', size='Preço', template='seaborn',
                                    title='Receita por Estado', hover_name='Local da compra', hover_data={'lat': False, 'lon': False},
                                    )

## Map Sell by State ##
vendas_estados     = df.groupby('Local da compra')['Local da compra'].count().rename('Vendas')
vendas_estados     = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(vendas_estados, left_on='Local da compra', right_index=True)
fig_vendas_estados = px.bar(vendas_estados.head(), x='Local da compra', y='Vendas', text_auto=True, title='Top Estados por vendas')

## Monthly Income ##
receita_mensal        = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month
fig_receita_mensal    = px.line(receita_mensal, x='Mes', y='Preço',
                                markers=True, range_y=(0, receita_mensal.max()),
                                color='Ano', line_dash='Ano', title='Receita Mensal')
fig_receita_mensal.update_layout(yaxis_title='Receita')

## Monthly sell ##
vendas_mensal        = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME')).size().reset_index(name='Vendas')
vendas_mensal['Ano'] = vendas_mensal['Data da Compra'].dt.year
vendas_mensal['Mes'] = vendas_mensal['Data da Compra'].dt.month
fig_vendas_mensal    = px.line(vendas_mensal, x='Mes', y='Vendas',
                               markers=True, range_y=(0, vendas_mensal.max()),
                               color='Ano', line_dash='Ano', title='Vendas Mensal')
fig_vendas_mensal.update_layout(yaxis_title='Vendas')

## Income per Category ##
receita_categoria     = df.groupby('Categoria do Produto')['Preço'].sum().sort_values(ascending=False)
fig_receita_categoria = px.bar(receita_categoria, text_auto=True, title='Receita por Categoria')

## Sell per Category ##
vendas_categoria     = df.groupby('Categoria do Produto').size().reset_index(name='Vendas').sort_values(by='Vendas', ascending=False)
fig_vendas_categoria = px.bar(vendas_categoria, x='Vendas', y='Categoria do Produto', text_auto=True, title='Vendas por Categoria')

## Seller Table ##
vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

#### Streamlit View ####

tab1, tab2, tab3 = st.tabs(['Receita', 'Quantidade de Vendas', 'Vendedores'])

## Receita ##
with tab1:
  col1, col2 = st.columns([2, 5])
  with col1:
    st.metric('Receita Total', format_number(df['Preço'].sum()), 'R$')
    st.plotly_chart(fig_map, use_container_width=True)
    st.plotly_chart(fig_receita_estados)
  with col2:
    st.metric('Nº de Vendas', format_number(df.shape[0]))
    st.plotly_chart(fig_receita_mensal, use_container_width=True)
    st.plotly_chart(fig_receita_categoria)

## Quantidade de Vendas ##
with tab2:
  col1, col2 = st.columns([2, 5])
  with col1:
    st.metric('Receita Total', format_number(df['Preço'].sum()), 'R$')
    n_estados = st.number_input('Quantidade de Estados', 1, vendas_estados.shape[0], 5)
    df_vendas_estados = vendas_estados.sort_values(by='Vendas', ascending=False).head(n_estados)
  with col2:
    st.metric('Nº de Vendas', format_number(df.shape[0]))

  col1, col2 = st.columns([2, 5])
  with col1:
    fig_map_vendas_estado = px.scatter_geo(df_vendas_estados,
                                          lat='lat', lon='lon', scope='south america', size='Vendas', template='seaborn',
                                          title=f'Top {n_estados} - Estados x Vendas', hover_name='Local da compra', hover_data={'lat': False, 'lon': False},
                                          )
    st.plotly_chart(fig_map_vendas_estado)
    fig_vendas_estados = px.bar(df_vendas_estados, x='Vendas', y=df_vendas_estados['Local da compra'],
                                  text_auto=True, title=f'Top {n_estados} - Estados x Vendas')
    st.plotly_chart(fig_vendas_estados)
  with col2:
    st.plotly_chart(fig_vendas_mensal, use_container_width=True)
    st.plotly_chart(fig_vendas_categoria, use_container_width=True)

## Vendedores ##
with tab3:
  n_vendedores = st.number_input('Quantidade de Vendedores', 2, 10, 5)
  col1, col2 = st.columns(2)
  with col1:
    st.metric('Receita Total', format_number(df['Preço'].sum()), 'R$')
    df_vendedores         = vendedores.sort_values(by='sum', ascending=False).head(n_vendedores)
    fig_receita_vendeores = px.bar(df_vendedores, x='sum', y=df_vendedores.index,
                                  text_auto=True, title=f'Top {n_vendedores} Receitas por Vendedor')
    st.plotly_chart(fig_receita_vendeores)
  with col2:
    st.metric('Nº de Vendas', format_number(df.shape[0]))
    df_vendedores         = vendedores.sort_values(by='count', ascending=False).head(n_vendedores)
    fig_vendas_vendeores = px.bar(df_vendedores, x='count', y=df_vendedores.index,
                                  text_auto=True, title=f'Top {n_vendedores} Vendas por Vendedor')
    st.plotly_chart(fig_vendas_vendeores)