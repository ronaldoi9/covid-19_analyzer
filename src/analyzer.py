from datetime import date, timedelta
import pandas as pd
import folium
import plotly.express as px

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


def make_folium_graph_map(brazilian_state_geo, cleared_brazilian_covid_19_data):

    # Initialize the map:
    graph_map = folium.Map([-15, -47], zoom_start=4)
    names = cleared_brazilian_covid_19_data['Province_State']
    folium.Choropleth(
        geo_data=brazilian_state_geo,
        name='choropleth',
        data=cleared_brazilian_covid_19_data,
        columns=['Province_State', 'Confirmed_05-23-2020'],
        key_on='feature.id',
        fill_color='YlOrBr',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Confirmed'
    ).add_to(graph_map)

    folium.LayerControl().add_to(graph_map)
    
    # Save to html
    graph_map.save('../graphics/brazilian_confirmed_cases_by_folium.html')

    return graph_map

def make_graph_map(region_geojson, dataFrame):
    
    fig = px.choropleth(dataFrame, geojson=region_geojson, locations='Province_State', color='Confirmed_05-23-2020',
                           color_continuous_scale="OrRd", featureidkey="properties.sigla",
                           center={"lat": -15, "lon": -47},
                           hover_name='Province_State',
                           range_color=(0, 50000),
                           scope='south america', template='plotly_dark',
                           labels={'Confirmed_05-23-2020':'Confirmed Cases'}
                          )
    fig.update_layout(margin={"r":0,"t":0,"l":1,"b":0})
    fig.write_html('../graphics/brazilian_confirmed_cases.html')

    return fig

def get_actual_day():
    return (date.today() - timedelta(1)).strftime('%m-%d-%Y')

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