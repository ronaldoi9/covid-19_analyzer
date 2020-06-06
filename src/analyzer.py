from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import os.path as path
import json

def get_brazilian_confirmed_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_confirmed_series.csv')

def get_brazilian_death_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_deaths_series.csv')

def get_brazilian_recovered_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_recovered_series.csv')

def get_brazilian_active_cases():
    return pd.read_csv('../data/brazilian covid-19 data/brazilian_active_series.csv')

def clean_unknown_rows_covid_19_df(df_region_covid_data):

    unknown_regions_index = df_region_covid_data.loc[df_region_covid_data['Province_State'] == 'Unknown'].index
    df_region_covid_data.drop(unknown_regions_index, inplace=True)
    
    brazilian_covid_19_data = df_region_covid_data[['Province_State', 'Country_Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']]

    return brazilian_covid_19_data

def get_initial_day():
    return date(2020, 5, 20)

def date_format(day):
    return day.strftime('%m-%d-%Y')

def get_number_of_collect_days():
    return (get_last_day_of_collection() - get_initial_day()).days

def get_dataframe_selected_by_option(options):

    if options == 'NÚMERO DE MORTOS':
        return get_brazilian_death_cases()
    elif options == 'CASOS RECUPERADOS':
        return get_brazilian_recovered_cases()
    elif options == 'CASOS ATIVOS':
        return get_brazilian_active_cases()
    else:
        return get_brazilian_confirmed_cases()

def filter_historic_df_by_cities(df_historic_cases, city, state):

    df_historic_cases = df_historic_cases.loc[df_historic_cases['estado'] == state]
    df_historic_cases = df_historic_cases.loc[df_historic_cases['municipio'] == city]

    return df_historic_cases

def filter_range_color(option):

    if option == 'NÚMERO DE MORTOS':
        return (0, 2500)
    elif option == 'CASOS RECUPERADOS':
        return (0, 50)
    elif option == 'CASOS ATIVOS':
        return (0, 50000)
    else:
        return (0, 40000)

def filter_map_color(option):

    if option == 'CASOS RECUPERADOS':
        return 'Greens'
    else:
        return 'OrRd'

def get_last_day_of_collection():

    last_day_of_collection = date.today()

    find_the_last_collect = True

    while find_the_last_collect:
        if path.exists(f'../data/world covid-19 data/{date_format(last_day_of_collection)}.csv'):
            find_the_last_collect = False
        else:
            last_day_of_collection = last_day_of_collection - timedelta(1)

    return last_day_of_collection

def get_cities_by_state(state_name, brazil_cities):
    df_uf_states = pd.read_csv('../data/brazilian geo data/uf-states.csv')

    df_uf_states = df_uf_states.loc[df_uf_states['nome'] == state_name]

    uf_state = df_uf_states['codigo_uf'].values[0]
    
    brazil_cities = brazil_cities.loc[brazil_cities['codigo_uf'] == uf_state]

    return brazil_cities['nome'].values

def get_lat_and_long(city_name, brazilian_cities_geo_data):

    city_lat_and_long = brazilian_cities_geo_data.loc[brazilian_cities_geo_data['nome'] == city_name]

    return {
        'lat': city_lat_and_long['latitude'].values[0],
        'lon': city_lat_and_long['longitude'].values[0]
    }

def get_covid_19_city_data(df_historic_cities, city_choised, option):

    df_historic_cities = df_historic_cities.loc[df_historic_cities['municipio'] == city_choised]

    length_data = len(df_historic_cities)

    if option == 'CASOS ACUMULADOS':
        return df_historic_cities['casosAcumulado'].values[length_data - 1]
    elif option == 'CASOS NOVOS':
        return df_historic_cities['casosNovos'].values[length_data - 1]
    elif option == 'ÓBITOS ACUMULADOS':
        return df_historic_cities['obitosAcumulado'].values[length_data - 1]
    else:
        return df_historic_cities['obitosNovos'].values[length_data - 1]
