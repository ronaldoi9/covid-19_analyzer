import pandas as pd
import json
from analyzer import clean_unknown_rows_covid_19_df, make_graph_map
from convert_state_name import convert_state_name_to_uf
 
brazilian_state_geo = 'brazilian geo data/brazil-states.geojson'
with open(brazilian_state_geo) as file:
    br_geo_data = json.load(file)    

brazilian_confirmed_series = pd.DataFrame()
brazilian_deaths_series = pd.DataFrame()
brazilian_recovered_series = pd.DataFrame()
brazilian_active_series = pd.DataFrame()

for day in range(20,24):
    covid_19_data = pd.read_csv(f'world covid-19 data/05-{day}-2020.csv')
    date = f'05-{day}-2020'

    brazilian_covid_19_data = covid_19_data.loc[covid_19_data['Country_Region'] == 'Brazil']
    brazilian_covid_19_data = clean_unknown_rows_covid_19_df(brazilian_covid_19_data)
    brazilian_covid_19_data['Province_State'] = brazilian_covid_19_data['Province_State'].apply(lambda state: convert_state_name_to_uf(state.upper()))

    brazilian_confirmed_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_confirmed_series[f'Confirmed_{date}'] = brazilian_covid_19_data['Confirmed'].values

    brazilian_deaths_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_deaths_series[f'Deaths_{date}'] = brazilian_covid_19_data['Deaths'].values

    brazilian_recovered_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_recovered_series[f'Recovered_{date}'] = brazilian_covid_19_data['Recovered'].values

    brazilian_active_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_active_series[f'Active_{date}'] = brazilian_covid_19_data['Active'].values

brazilian_confirmed_series.to_csv('brazilian covid-19 data/brazilian_confirmed_series.csv', index=False)
brazilian_deaths_series.to_csv('brazilian covid-19 data/brazilian_deaths_series.csv', index=False)
brazilian_recovered_series.to_csv('brazilian covid-19 data/brazilian_recovered_series.csv', index=False)
brazilian_active_series.to_csv('brazilian covid-19 data/brazilian_active_series.csv', index=False)