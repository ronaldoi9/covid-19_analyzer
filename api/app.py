import json, sys
sys.path.append('/home/ronaldo/Documentos/Python Projects/Covid-19 Analyzer/src/')
import streamlit as st
import plotly.express as px
from analyzer import get_initial_day, date_format, get_last_day_of_collection
from analyzer import filter_data_distribution_to_show, filter_range_color, filter_map_color

# st.cache tag indicate that func must be stay in cache to speed up process
@st.cache(allow_output_mutation=True)
def get_brazilian_geo_data():
    with open('../data/brazilian geo data/brazil-states.geojson') as file:
        return json.load(file)

brazilian_geo_data = get_brazilian_geo_data()

# Side bar Menu
st.sidebar.title("Análise")

button_analyze = st.sidebar.radio("Selecione o tipo de análise que deseja realizar", 
                ('ESTADOS', 'CIDADES'))

st.sidebar.title("Data de Análise")

days_ago = st.sidebar.date_input(f'Selecione a data que deseja analisar', value=get_last_day_of_collection(), min_value=get_initial_day(), max_value=get_last_day_of_collection())


st.title(f"Analisando o impacto da COVID-19 no Brasil")

# subtitle
st.markdown("Este Data App foi construido para analisar os diferentes cenários de COVID-19 no Brasil")

option_selected = st.selectbox(
  'Selecione a opção que deseja analisar',
  ('CASOS CONFIRMADOS', 'NÚMERO DE MORTOS', 'CASOS RECUPERADOS', 'CASOS ATIVOS'))

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

day = date_format(days_ago)

# filter interest to show in graph
data_to_show = filter_data_distribution_to_show(option_selected)

with st.spinner('Carregando gráfico...'):
  # plot data distribution
  if button_analyze == 'ESTADOS':
    figure = make_graph_map(data_to_show, option_selected, day)
  else:
    pass
    # make figure to cities

st.plotly_chart(figure)
