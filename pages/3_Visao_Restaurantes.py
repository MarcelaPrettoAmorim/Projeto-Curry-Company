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
import numpy as np

st.set_page_config(page_title = 'Visão Restaurantes', layout = 'wide', page_icon = '🥡')

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

def distance(df1, fig):
    if fig == False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

        df1['distance'] = df1.loc[:, cols].apply( lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

        distancia_media = np.round(df1['distance'].mean(), 2)
            
        return distancia_media
    
    else:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']

        df1['distance'] = df1.loc[:, cols].apply( lambda x: haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), (x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis = 1)

        distancia_media = df1.loc[:, ['City','distance']].groupby('City').mean().reset_index()
        
        fig = go.Figure(data=[go.Pie(labels = distancia_media['City'], values = distancia_media['distance'], pull = [0, 0.1, 0])])
        
        return fig
        

def avg_std_time_delivery(df1, festival, op):
    """
        Esta função calcula o tempo médio e o desvio padrão do tempo de entrega
        Parâmetros:
            Input:
                -df: dataframe com os dados necessário para o cálculo
                -op: tipo de operação que precisa ser calculado
                     'avg_time": calcula o tempo médio
                     'std_time': calcula o desvio padrão do tempo
            Output:
                -df: dataframe com 2 colunas e 1 linhas
    """
    if op == 'avg':
        df_aux = (df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').agg({'Time_taken(min)': ['mean',    'std']}))
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()

        # Selecionando somente a condição onde Festival = Yes
        df_aux = np.round(df_aux.loc[df_aux['Festival'] == festival, op], 2)     
        
    return df_aux

def avg_std_time_graph(df1):
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg({'Time_taken(min)': ['mean', 'std']})
        
    df_aux.columns = ['T. medio', 'DP tempo']
    df_aux = df_aux.reset_index()
            
    fig = go.Figure()
    fig.add_trace(go.Bar(name = 'Control', x = df_aux['City'], y = df_aux['T. medio'], error_y = dict(type = 'data', array = df_aux['DP tempo'])))
    fig.update_layout(barmode = 'group')
                
    return fig

def avg_std_time_on_traffic(df1):
    cols = ['City','Road_traffic_density', 'Time_taken(min)']

    df_aux = df1.loc[:, cols].groupby(['City','Road_traffic_density']).agg({'Time_taken(min)': ['mean', 'std']})

    df_aux.columns = ['T. médio', 'DP tempo']

    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux, path = ['City', 'Road_traffic_density'], values = 'T. médio', color = 'DP tempo', color_continuous_scale = 'RdBu', color_continuous_midpoint = np.average(df_aux['DP tempo']))
                
    return fig

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

#Visão Restaurantes

# -----------------------------------
#    Barra lateral do Streamlit
# -----------------------------------
st.header('Marketplace - Visão Restaurantes')

#image_path = 'Logo.png'
image = Image.open('Logo.jpg')
st.sidebar.image(image, width = 240)

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
    
        
        col1, col2, col3, col4, col5, col6 = st.columns(6, gap = 'small')
        
        with col1:
            #Calcular a quantidade de entregadores únicos cadastrados
            entregador_unico = len(df1['Delivery_person_ID'].unique())
        
            #Imprimir resposta
            col1.metric('Entregadores únicos', entregador_unico)
            
        with col2:
            distancia_media = distance(df1, fig = False)
            col2.metric('A distância média das entregas', distancia_media)
            
            
        with col3:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'avg_time')
            #col3.metric('T. medio de entrega com Festival', df_aux)
            
            #df_aux = df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').mean().reset_index()

            #Remover linhas com valores vazios na coluna Festival
            #df1 = df1.loc[(df1['Festival'] != 'NaN'), :].copy()

            # Selecionando somente a condição onde Festival = Yes
            #df_aux = np.round(df_aux.loc[(df_aux['Festival'] == 'Yes'), 'Time_taken(min)'], 2)
            
            col3.metric('T. medio de entrega com Festival', df_aux)
            
        with col4:
            df_aux = avg_std_time_delivery(df1, 'Yes', 'std_time')
            col4.metric('DP de entrega com Festival', df_aux)
            
        with col5:
            df_aux = avg_std_time_delivery(df1, 'No', 'avg_time')
            col5.metric('T. medio de entrega sem Festival', df_aux)
        
        with col6:
            df_aux = avg_std_time_delivery(df1, 'No', 'std_time')
            col6.metric('DP de entrega sem Festival', df_aux)
            
        
    with st.container():
        st.markdown("""---""")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = avg_std_time_graph(df1)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            df_aux = df1.loc[:, ['City','Type_of_order', 'Time_taken(min)']].groupby(['City','Type_of_order']).agg({'Time_taken(min)': ['mean', 'std']})

            df_aux.columns = ['T. médio', 'DP tempo']

            df_aux = df_aux.reset_index()

            st.dataframe(df_aux, use_container_width=True)
   
    with st.container():
        st.title('Distribuição de tempo')
    
        col1, col2 = st.columns(2)
        with col1:
            fig = distance(df1, fig = True)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = avg_std_time_on_traffic(df1)    
            st.plotly_chart(fig, use_container_width=True)
               
    
       
