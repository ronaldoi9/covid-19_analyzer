import pandas as pd
import json
from datetime import date, timedelta
from analyzer import clean_unknown_rows_covid_19_df, make_graph_map
from convert_state_name import convert_state_name_to_uf
 
brazilian_state_geo = '../data/brazilian geo data/brazil-states.geojson'
with open(brazilian_state_geo) as file:
    br_geo_data = json.load(file)    

brazilian_confirmed_series = pd.DataFrame()
brazilian_deaths_series = pd.DataFrame()
brazilian_recovered_series = pd.DataFrame()
brazilian_active_series = pd.DataFrame()

# get the actual day
today = date.today()

# search start day
initial_day = date(2020, 5, 20)

# difference of days
number_of_days = (today - initial_day).days

for day in [initial_day + timedelta(i) for i in range(number_of_days)]:
    day = day.strftime('%m-%d-%Y')
    covid_19_data = pd.read_csv(f'../data/world covid-19 data/{day}.csv')

    brazilian_covid_19_data = covid_19_data.loc[covid_19_data['Country_Region'] == 'Brazil']
    brazilian_covid_19_data = clean_unknown_rows_covid_19_df(brazilian_covid_19_data)
    brazilian_covid_19_data['Province_State'] = brazilian_covid_19_data['Province_State'].apply(lambda state: convert_state_name_to_uf(state.upper()))

    brazilian_confirmed_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_confirmed_series[f'{day}'] = brazilian_covid_19_data['Confirmed'].values

    brazilian_deaths_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_deaths_series[f'{day}'] = brazilian_covid_19_data['Deaths'].values

    brazilian_recovered_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_recovered_series[f'{day}'] = brazilian_covid_19_data['Recovered'].values

    brazilian_active_series[f'Province_State'] = brazilian_covid_19_data['Province_State'].values
    brazilian_active_series[f'{day}'] = brazilian_covid_19_data['Active'].values

brazilian_confirmed_series.to_csv('../data/brazilian covid-19 data/brazilian_confirmed_series.csv', index=False)
brazilian_deaths_series.to_csv('../data/brazilian covid-19 data/brazilian_deaths_series.csv', index=False)
brazilian_recovered_series.to_csv('../data/brazilian covid-19 data/brazilian_recovered_series.csv', index=False)
brazilian_active_series.to_csv('../data/brazilian covid-19 data/brazilian_active_series.csv', index=False)