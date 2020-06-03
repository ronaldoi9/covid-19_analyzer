from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import os.path as path

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

def filter_data_distribution_to_show(options):

    if options == 'NÚMERO DE MORTOS':
        return get_brazilian_death_cases()
    elif options == 'CASOS RECUPERADOS':
        return get_brazilian_recovered_cases()
    elif options == 'CASOS ATIVOS':
        return get_brazilian_active_cases()
    else:
        return get_brazilian_confirmed_cases()

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