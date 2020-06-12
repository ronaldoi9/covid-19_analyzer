import json, sys
sys.path.append('/home/ronaldo/Documentos/Python Projects/Covid-19 Analyzer/src/')
import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import numpy as np
from os import path
from analyzer import get_initial_day, date_format, get_last_day_of_collection, get_cities_by_state, get_lat_and_long, get_covid_19_city_data, get_capital_index
from analyzer import get_dataframe_selected_by_option, filter_range_color, filter_map_color, filter_historic_df_by_cities

# st.cache tag indicate that func must be stay in cache to speed up process
@st.cache(allow_output_mutation=True)
def get_brazilian_geo_data():
    with open('../data/brazilian geo data/brazil-states.geojson') as file:
        return json.load(file)

@st.cache(allow_output_mutation=True)
def get_brazilian_cities():
    return pd.read_csv('../data/brazilian geo data/brazil-cities.csv', low_memory=False)

@st.cache()
def get_brazilian_historic_data_frame():
    return pd.read_csv('../data/brazilian covid-19 data/historic.csv', low_memory=False)

brazilian_geo_data = get_brazilian_geo_data()
brazilian_cities_geo_data = get_brazilian_cities()

# =====================================================================================
# Side bar Menu
st.sidebar.title("Análise")

button_analyze = st.sidebar.radio("Selecione o tipo de análise que deseja realizar", 
                ('ESTADOS', 'CIDADES'))

if button_analyze == 'CIDADES':
  st.sidebar.title("Escolha o estado da cidade")

  brazilian_states = ['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará', 'Distrito Federal', 'Espirito Santo', 'Goiás', 
                        'Maranhão', 'Mato Grosso do Sul', 'Mato Grosso', 'Minas Gerais', 'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 
                        'Piauí', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 
                        'São Paulo', 'Sergipe', 'Tocantins']

  state_choised = st.sidebar.selectbox(
      'Selecione ou digite estado', brazilian_states, index=12)

st.sidebar.title("Data de Análise")

days_ago = st.sidebar.date_input(f'Selecione a data que deseja analisar', value=get_last_day_of_collection(), min_value=get_initial_day(), max_value=get_last_day_of_collection())

# =====================================================================================

st.title(f"Analisando o impacto da COVID-19 no Brasil")

# subtitle
st.markdown("Este Data App foi construido para analisar os diferentes cenários de COVID-19 no Brasil")

if button_analyze == 'CIDADES':

  city_data = []
  df_cities = get_brazilian_historic_data_frame()

  option_selected = st.selectbox(
  'Selecione a opção que deseja analisar',
  ('CASOS ACUMULADOS', 'CASOS NOVOS', 'ÓBITOS ACUMULADOS', 'ÓBITOS NOVOS'))

  st.subheader('Informe o nome da cidade que deseja analisar')

  cities_by_state = get_cities_by_state(state_choised, brazilian_cities_geo_data)
  capital_index = get_capital_index(state_choised, cities_by_state)

  city_choised = st.selectbox(
    'Selecione ou digite o nome da cidade', 
    cities_by_state, index=capital_index)

  lat_and_lon = get_lat_and_long(city_choised, brazilian_cities_geo_data)
  covid_19_city_data = get_covid_19_city_data(df_cities, city_choised, option_selected)

  city_data.append({
      'n_casos': covid_19_city_data,
      'lat': lat_and_lon['lat'],
      'lon': lat_and_lon['lon']
  })

  compare_city = st.radio(
      "Deseja comparar cidades?",
      ('Sim', 'Não'), index=1)

  if compare_city == 'Sim':

    index_to_exclude = list(cities_by_state).index(city_choised)
    cities_by_state = list(cities_by_state)

    del((cities_by_state[index_to_exclude]))

    city_to_compare = st.selectbox(
      'Selecione ou digite o nome da cidade para comparar', 
      cities_by_state, index=capital_index+1)

    if st.button('Adicionar cidade no gráfico'):
      covid_19_city_data = get_covid_19_city_data(df_cities, city_to_compare, option_selected)
      lat_and_lon = get_lat_and_long(city_to_compare, brazilian_cities_geo_data)

      city_data.append({
        'n_casos': covid_19_city_data,
        'lat': lat_and_lon['lat'],
        'lon': lat_and_lon['lon']
      })
else:
  option_selected = st.selectbox(
    'Selecione a opção que deseja analisar',
    ('CASOS CONFIRMADOS', 'NÚMERO DE MORTOS', 'CASOS RECUPERADOS', 'CASOS ATIVOS'))

  data_to_show = get_dataframe_selected_by_option(option_selected)

st.subheader("COVID-19 no Brasil")

def make_graph_map(dataFrame, option, day):

    color_scale = filter_map_color(option)
    range_color = filter_range_color(option)
    dataFrame.rename(columns={'Province_State': 'Estado'}, inplace=True)

    fig = px.choropleth(dataFrame, geojson=brazilian_geo_data, locations='Estado', color=day,
                          color_continuous_scale=color_scale, featureidkey="properties.sigla",
                          center={"lat": -19, "lon": -65},
                          hover_name='Estado',
                          range_color=range_color,
                          scope='south america', template='plotly_dark',
                          labels={day:f'{option}'})
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def make_cities_graph(cities_data):
  dframes = []
  layers = []  

  for i in range(len(cities_data)):
    dframes.append(pd.DataFrame(np.random.randn(cities_data[i]['n_casos'], 2) / [30,50] + [cities_data[i]['lat'], cities_data[i]['lon']], 
                  columns=['lat', 'lon']))

    elevation_rage = [0, (cities_data[i]['n_casos'])/100]
    layers.append(pdk.Layer(
          'HexagonLayer',
          data=dframes[i],
          get_position='[lon, lat]',
          auto_highlight=True,
          radius=200,
          elevation_scale=50,
          elevation_range=elevation_rage,
          pickable=True,
          extruded=True,
          coverage=1))

    if (cities_data[i]['n_casos']) > 60000:
      zoom = 9
    elif (cities_data[i]['n_casos']) > 23000:
      zoom = 10
    else:
      zoom = 11

  st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=cities_data[len(cities_data) - 1]['lat'],
        longitude=cities_data[len(cities_data) - 1]['lon'], 
        zoom=zoom,
        pitch=50),
    layers=[layers],
    ))
  
day = date_format(days_ago)

with st.spinner('Carregando gráfico...'):
  # plot data distribution
  if button_analyze == 'ESTADOS':
    figure = make_graph_map(data_to_show, option_selected, day)
    st.plotly_chart(figure)
  else:    
    st.info(f'{option_selected}: {covid_19_city_data}')
    make_cities_graph(city_data)

