import streamlit as st
from PIL import Image


st.set_page_config(
    page_title = 'Home',
    layout = 'wide',
    page_icon = '🍴'
)

image = Image.open('food_logo.png')
st.sidebar.image(image, width = 240)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write('# Curry Company Growth Dashboard')

st.markdown(
    """
    Growth Dashboard construído para acompanhar as métricas de crescimento de entregadores e restaurantes.
    ### Sobre esse Growth Dashboard:
    - Visão Empresa:
        - *Visão Gerencial: métricas gerais de comportamento*.
        - *Visão Tática: indicadores semanais de crescimento*.
        - *Visão Geográfica: Insights de geolocalização*.
    - Visão Entregador:
        - *Acompanhamento dos indicadores semanais de crescimento*.
    - Visão Restaurantes:
        - *Indicadores semanais de crescimento dos restaurantes*.
    ### Contato
    - LinkedIn: [Marcela Amorim](https://www.linkedin.com/in/marcela-de-pretto-amorim/).
    """)
