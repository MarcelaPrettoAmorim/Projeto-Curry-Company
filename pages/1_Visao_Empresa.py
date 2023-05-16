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

st.set_page_config(page_title = 'Visão Empresa', layout = 'wide', page_icon = '📈')

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

def order_metric(df1):
    # Selecionar colunas necessárias 
    cols =  ['ID', 'Order_Date']

    # Selecionar linhas e realizar a contagem agrupando por dia
    df_aux = df1.loc[:, cols].groupby('Order_Date').count().reset_index().copy()

    # Desenhar gráfico de barras usando biblioteca Plotly
    fig = px.bar(df_aux, x = 'Order_Date', y = 'ID')
            
    return fig
        
def traffic_order_share(df1):
    # Selecionar linhas necessárias
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index().copy()

    # Remover valores nulos da coluna Road_traffic_density
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

    # Criar coluna auxiliar com as porcentagens por cada tipo de tráfego
    df_aux['Porcentagem_trafego'] = df_aux['ID']/df_aux['ID'].sum()

    # Desenhar gráfico de pizza usando biblioteca Plotly
    fig = px.pie(df_aux, values = 'Porcentagem_trafego', names = 'Road_traffic_density')
                
    return fig
                        
def traffic_order_city(df1)          :  
    # Selecionar linhas e agrupar por cidade e por tipo de tráfego
    df_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density']).count().reset_index().copy()
        
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

    # Desenhar gráfico de bolhas usando biblioteca Plotly
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
                        
    return fig
                        
def order_by_week(df1):
    # Criar coluna da semana
    # comando dt = transforma de series para data a coluna Order_Date
    # Comando strftime = seleciona a coluna do ano a data está
    # %U determina que o primeiro dia da semana seja domingo
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime("%U")

    # Selecionar linhas e realizar a contagem agrupando por semana
    df_aux = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index().copy()

    # Desenhar gráfico de linhas usando biblioteca Plotly
    fig = px.line(df_aux, x = 'Week_of_year', y = 'ID')
        
    return fig
                        
def order_share_by_week(df1):                
    # Calcular quantidade de pedidos por semana
    df_aux1 = df1.loc[:, ['ID', 'Week_of_year']].groupby('Week_of_year').count().reset_index().copy()

    # Calcular a quantidade de entregadores únicos por semana
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby('Week_of_year').nunique().reset_index().copy()

    # Unir os dois dataframes gerados
    df_aux = pd.merge(df_aux1, df_aux2, how = 'inner')

    # Dividir a quantidade de entregas por semana pela quantidade de 
    # entregadores únicos da semana
    df_aux['Order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    # Desenhar gráfico de linha usando biblioteca Plotly
    fig =  px.line(df_aux, x = 'Week_of_year', y = 'Order_by_deliver')
        
    return fig
                        
def country_maps(df1):
    # Selecionar linhas necessárias e agrupar por cidade e tipo de tráfego
    df_aux = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby(['City', 'Road_traffic_density']).median().reset_index().copy()
    
    # Criar mapa
    map = folium.Map()
    
    for index, location_info in df_aux.iterrows():
        folium.Marker([location_info['Delivery_location_latitude'],location_info['Delivery_location_longitude']], popup = location_info[['City','Road_traffic_density']]).add_to(map)
        
    folium_static(map, width = 1024, height =600) 
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

#Visão Empresa

# -----------------------------------
#    Barra lateral do Streamlit
# -----------------------------------
st.header('Marketplace - Visão Cliente')

#image_path = 'Logo.png'
image = Image.open('Logo.png')
st.sidebar.image(image, width = 120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime(2022, 4, 13),
    min_value = pd.datetime(2022, 2, 11),
    max_value = pd.datetime(2022, 4, 6),
    format = 'DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito?',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low','Medium', 'High', 'Jam'])

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

# Filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

st.dataframe(df1)
# -----------------------------------
#         Layout no Streamlit
# -----------------------------------
tab1, tab2, tab3 = st.tabs(['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        #Order metric
        fig = order_metric(df1)
        st.markdown('# Orders by Day')
        st.plotly_chart(fig, use_container_width = True)
        

    with st.container(): 
        col1, col2 = st.columns(2)
        with col1:
            st.header('Traffic Order Share')
            fig = traffic_order_share(df1)
            st.plotly_chart(fig, use_container_width = True)
           
            
        with col2:
            st.header('Traffic Order City')
            fig = traffic_order_city(df1)
            st.plotly_chart(fig, use_container_width = True)
            
with tab2:
    with st.container():
        st.header('Order by Week')
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width = True)
        
    with st.container():
        st.header('Order Share by Week')
        fig = order_share_by_week(df1)
        st.plotly_chart(fig, use_container_width = True)

    
with tab3:
    st.header('Country Maps')
    country_maps(df1)
   
    
    
                        


