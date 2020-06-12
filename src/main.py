import pandas as pd
import json
from datetime import date, timedelta
from convert_state_name import convert_state_name_to_uf
from analyzer import clean_unknown_rows_covid_19_df, get_initial_day, date_format, get_last_day_of_collection, get_number_of_collect_days

brazilian_historic = pd.read_excel(f'../data/brazilian covid-19 data/HIST_PAINEL_COVIDBR_11jun2020.xlsx')
brazilian_historic.drop(columns=['Recuperadosnovos', 'emAcompanhamentoNovos', 'semanaEpi', 
                                'codRegiaoSaude', 'coduf', 'codmun', 'nomeRegiaoSaude'], 
                                inplace=True)
                                
brazilian_historic = brazilian_historic.dropna()
brazilian_historic.to_csv('../data/brazilian covid-19 data/historic.csv', index=False)


brazilian_confirmed_series = pd.DataFrame()
brazilian_deaths_series = pd.DataFrame()
brazilian_recovered_series = pd.DataFrame()
brazilian_active_series = pd.DataFrame()

# get the actual day
today = date.today()

initial_day = get_initial_day()

# number of days collected
number_of_days = get_number_of_collect_days()

for day in [initial_day + timedelta(i) for i in range(number_of_days + 1)]:
    day = date_format(day)
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