import pandas as pd
import json
import streamlit as st
import plotly.express as px

# function to load treated boston dataset
# st.cache tag indicate that func must be stay in cache to speed up process
@st.cache
def get_brazilian_geo_data():
    with open('../data/brazilian geo data/brazil-states.geojson') as file:
        return json.load(file)
@st.cache
def get_brazilian_confirmed_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_confirmed_series.csv')
@st.cache
def get_brazilian_death_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_deaths_series.csv')
@st.cache
def get_brazilian_recovered_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_recovered_series.csv')
@st.cache
def get_brazilian_active_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_active_series.csv')

brazilian_geo_data = get_brazilian_geo_data()
brazilian_confirmed_cases = get_brazilian_confirmed_cases()
brazilian_deaths_cases = get_brazilian_death_cases()
brazilian_recovered_cases = get_brazilian_recovered_cases()
brazilian_active_cases = get_brazilian_active_cases()

st.title("Data App - Analisando o impacto da COVID-19 nos estados brasileiros")

# subtitle
st.markdown("Este Data App foi construido para analisar os diferentes cenários de COVID-19 no Brasil")

options = st.selectbox(
  'Selecione o que deseja analisar',
  ('Casos confirmados', 'Número de Mortos', 'Casos Recuperados', 'Casos ativos'))

st.subheader("COVID-19 no Brasil")

def make_graph_map(dataFrame, options, day):
    if options == 'Casos Recuperados':
        color_scale = 'Greens'
    else:
        color_scale = 'OrRd'
    fig = px.choropleth(dataFrame, geojson=brazilian_geo_data, locations='Province_State', color=day,
                           color_continuous_scale=color_scale, featureidkey="properties.sigla",
                           center={"lat": -15, "lon": -47},
                           hover_name='Province_State',
                           range_color=(0, 50000),
                           scope='south america', template='plotly_dark',
                           labels={day:f'{options}'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

data = brazilian_confirmed_cases

if options == 'Número de Mortos':
    data = brazilian_deaths_cases
elif options == 'Casos Recuperados':
    data = brazilian_recovered_cases
elif options == 'Casos ativos':
    data = brazilian_active_cases

day = '05-23-2020'
# plot data distribution
figure = make_graph_map(data, options, day)
st.plotly_chart(figure)