# Covid-19 Analyzer
![cities_comparison](https://user-images.githubusercontent.com/40616142/84558536-f2eab380-ad09-11ea-829b-ac980af4b41b.gif)
## About this project
Main goal:  
  
*"Analyze the different covid-19 scenarios in Brazilian states and cities"* <span>&#x1f1e7;&#x1f1f7;</span>

## Why?
Brazil being a very large country, there are several scenarios to be analyzed, some cities are already facing a drop in the number of cases, and others they are starting to face the pandemic. Then this data app will be able to inform users about the situation about their city's covid-19.

## Datas
Data were collected from two different sources
- **States:**  
To analyze the covid-19 information from the states, was used data from the [Center for Systems Science and Engineering (CSSE) at Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19).
- **Cities:**  
To analyze the covid-19 information from the cities, was used data from the government of Brazil, that can be found [here](https://covid.saude.gov.br/).

## Functionalities
- **Cities analyzer**  

  - Information about the covid-19 of all brazilian cities  
  
  - Comparison of different scenarios about covid-19 in cities in the same state  
  
  - Information about:  
    - Accumulated Cases
    - New Cases
    - Accumulated Deaths
    - New Deaths
    
- **States analyzer**  

  - Information about the covid-19 of all brazilian states  
  
  - Change analyze date  
  
  - Information about:  
    - Confirmed Cases
    - Number of Deaths
    - Recovered Cases
    - Active Cases
    
## Built With
- [Streamlit](https://www.streamlit.io/) - Build the data app
- [Pandas](https://pandas.pydata.org/) - Read data informations about covid-19
- [Plotly](https://plotly.com/) - States map
- [Pydeck](https://pypi.org/project/pydeck/) - Cities map
- [Numpy](https://numpy.org/) - Samples distribution to cities map.
