import json, sys
sys.path.append('/home/ronaldo/Documentos/Python Projects/Covid-19 Analyzer/src/')
import streamlit as st
import plotly.express as px
from analyzer import get_number_of_collect_days, convert_day_number_to_date
from analyzer import filter_data_distribution_to_show, filter_range_color, filter_map_color

# st.cache tag indicate that func must be stay in cache to speed up process
@st.cache(allow_output_mutation=True)
def get_brazilian_geo_data():
    with open('../data/brazilian geo data/brazil-states.geojson') as file:
        return json.load(file)

brazilian_geo_data = get_brazilian_geo_data()

st.title("Analisando o impacto da COVID-19 nos estados brasileiros")

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


number_of_days = get_number_of_collect_days() - 1

# show by default the actual day
days_ago = st.slider(f'LINHA TEMPORAL DE {option_selected}', (number_of_days * -1), -1, format=f'%d Dias')

day = convert_day_number_to_date(days_ago)

# filter interest to show in graph
data_to_show = filter_data_distribution_to_show(option_selected)

with st.spinner('Carregando gráfico'):
  # plot data distribution
  figure = make_graph_map(data_to_show, option_selected, day)
st.success('Concluído!')

st.plotly_chart(figure)


# Side bar Menu
st.sidebar.title("Análise")

botao_selected = st.sidebar.radio("Selecione o tipo de análise que deseja realizar", 
                ('ESTADOS', 'CIDADES'))
