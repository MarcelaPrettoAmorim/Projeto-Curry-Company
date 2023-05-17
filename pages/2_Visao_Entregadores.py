#Libraries
import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime
from PIL import Image
import folium 
from streamlit_folium import folium_static

st.set_page_config(page_title = 'Visão Entregadores', layout = 'wide', page_icon = '🛺')
#-----------------------------------------
#                  FUNÇÕES
#-----------------------------------------
def clean_code(df1):
    """ Esta funcao tem a responsabilidade de limpar o dataframe
    
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços das variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)
        
        Input: dataframe
        Output: dataframe
    
    """
    # Remover linhas nulas da coluna Delivery_person_Age e converter para tipo inteiro
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # Remover linhas nulas da coluna Road_traffic_density
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # Remover linhas nulas da coluna City
    linhas_selecionadas = (df1['City'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # Remover linhas nulas da coluna Festival
    linhas_selecionadas = (df1['Festival'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # Remover linhas nulas da coluna multiple_deliveries e converter para tipo inteiro
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # Converter a coluna Delivery_person_Ratings para tipo decimal
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # Converter a coluna Order_Date para tipo data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format = '%d-%m-%Y')

    # Remover espaços das colunas
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()

    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split('(min) ')[1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    
    return df1

def top_delivers(df1, top_asc):
    # Ordenar os valores de tempo de entrega por cidade
    df2 = df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']].groupby(['City', 'Delivery_person_ID']).mean().sort_values(['City','Time_taken(min)'], ascending = top_asc).reset_index()

    #Selecionar os 10 primeiros que representam os entregadores mais rápidos(menor tempo)
    df_aux1 = df2.loc[df2['City'] == 'Metropolitian', :]. head(10)
    df_aux2 = df2.loc[df2['City'] == 'Urban', :]. head(10)
    df_aux3 = df2.loc[df2['City'] == 'Semi-Urban', :]. head(10)

    #Unir os dataframes gerados
    df3 = pd.concat([df_aux1, df_aux2, df_aux3]).reset_index(drop = True)
    
    return df3
#--------------------------Início da Estrutura Lógica do código--------------------------
#-----------------------------------------
# Importar dataset
#-----------------------------------------
df = pd.read_csv('dataset/train.csv')

#-----------------------------------------
# Limpeza do dataframe
#-----------------------------------------
df1 = df.copy()
df1 = clean_code(df1)

#Visão Entregadores

# -----------------------------------
#    Barra lateral do Streamlit
# -----------------------------------
st.header('Marketplace - Visão Entregadores')

#image_path = 'Logo.png'
image = Image.open('Logo.png')
st.sidebar.image(image, width = 120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.to_datetime('2022-04-13').to_pydatetime(),
    min_value=pd.to_datetime('2022-02-11').to_pydatetime(),
    max_value=pd.to_datetime('2022-04-06').to_pydatetime(),
    format='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low','Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")

climatic_options = st.sidebar.multiselect(
    'Quais as condições de clima?',
    ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'],
    default = ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 'conditions Stormy', 'conditions Sunny', 'conditions Windy'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de clima
linhas_selecionadas = df1['Weatherconditions'].isin(climatic_options)
df1 = df1.loc[linhas_selecionadas, :]

# -----------------------------------
#         Layout no Streamlit
# -----------------------------------

tab1, tab2, tab3 = st.tabs(['Visão Gerencial', '-', '-'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1, col2, col3, col4 = st.columns(4, gap = 'large')
        with col1:
            maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
            col1.metric('Maior idade', maior_idade)
            
        with col2:
            menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
            col2.metric('Maior idade', menor_idade)
            
        with col3:
            melhor_condicao = df1.loc[:, 'Vehicle_condition'].max()
            col3.metric('Melhor condição', melhor_condicao)
            
        with col4:
            pior_condicao = df1.loc[:, 'Vehicle_condition'].min()
            col4.metric('Pior condição', pior_condicao)
                
                
    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('##### Avaliação média por entregador')
            
            #Calcular a média das avaliações agrupando por entregador
            aval_media_entregador = df1.loc[:,['Delivery_person_Ratings', 'Delivery_person_ID']].groupby('Delivery_person_ID').mean().reset_index()
            st.dataframe(aval_media_entregador)
            
        with col2:
            st.markdown('##### Avaliação média por trâsito')
             # Calcular a média e o desvio padrão das avaliações agrupando por tipo de tráfego
            # Utilizar a função agg
            aval_media_transito = df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']].groupby('Road_traffic_density').agg({'Delivery_person_Ratings': ['mean','std']})

            # Renomear as colunas
            aval_media_transito.columns = ['Delivery_mean', 'Delivery_std']

            #Resetar o index nesta etapa para corrigir formato do dataframe
            aval_media_transito.reset_index()
            
            # Imprimir resposta
            st.dataframe(aval_media_transito)
            
            
            st.markdown('##### Avaliação média por clima')
            # Calcular a média e o desvio padrão das avaliações agrupando por tipo de tráfego
            # Utilizar a função agg
            aval_media_clima = df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']].groupby('Weatherconditions').agg({'Delivery_person_Ratings' : ['mean', 'std']})

            #Renomear as colunas
            aval_media_clima.columns = ['Delivery_mean', 'Delivery_std']

            #Resetar o index nesta etapa para corrigir formato do dataframe
            aval_media_clima.reset_index()
            
            # Imprimir resposta
            st.dataframe(aval_media_clima)
            
    with st.container():
        st.markdown("""---""")
        st.title('Velocidade de entrega')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Top entregadores mais rápidos')
            df3 = top_delivers(df1, top_asc = True)
            st.dataframe(df3)
            
        with col2:
            st.subheader('Top entregadores mais lentos')
            df3 = top_delivers(df1, top_asc = False)
            st.dataframe(df3)
