import pandas as pd
import json
import streamlit as st
from analyzer import make_graph_map

# function to load treated boston dataset
# st.cache tag indicate that func must be stay in cache to speed up process
@st.cache
def get_data():
    return pd.read_csv('brazilian covid-19 data/brazilian_confirmed_series.csv')

@st.cache
def get_brazilian_geo_data():
    with open('brazilian geo data/brazil-states.geojson') as file:
        return json.load(file)

data = get_data()
brazilian_geo_data = get_brazilian_geo_data()

st.title("Data App - Analisando o impacto da COVID-19 nos estados brasileiros")

# subtitle
st.markdown("Este Data App foi construido para analisar os diferentes cenários de COVID-19 no Brasil")

# verificando o dataset
st.subheader("Selecionando apenas um pequeno conjunto de atributos")

# default attributes to show
defaultcols = ["Province_State", "Confirmed_05-23-2020"]

# define attributes by multiselect
cols = st.multiselect("Atributos", data.columns.tolist(), default=defaultcols)

# show dataframe top 10
st.dataframe(data[cols])

st.subheader("COVID-19 no Brasil")

# plot data distribution
figure = make_graph_map(brazilian_geo_data, data)
st.plotly_chart(figure)