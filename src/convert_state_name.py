
def convert_state_name_to_uf(state_name):

    switcher = {
    "ACRE": "AC",
    "ALAGOAS": "AL",
    "AMAZONAS": "AM",
    "AMAPA": "AP",
    "BAHIA": "BA",
    "CEARA": "CE",
    "DISTRITO FEDERAL": "DF",
    "ESPIRITO SANTO": "ES",
    "GOIAS": "GO",
    "MARANHAO": "MA",
    "MINAS GERAIS": "MG",
    "MATO GROSSO DO SUL": "MS",
    "MATO GROSSO": "MT",
    "PARA": "PA",
    "PARAIBA": "PB",
    "PERNAMBUCO": "PE",
    "PIAUI": "PI",
    "PARANA": "PR",
    "RIO DE JANEIRO": "RJ",
    "RIO GRANDE DO NORTE": "RN",
    "RONDONIA": "RO",
    "RORAIMA": "RR",
    "RIO GRANDE DO SUL": "RS",
    "SANTA CATARINA": "SC",
    "SERGIPE": "SE",
    "SAO PAULO": "SP",
    "TOCANTINS": "TO",
    }

    return switcher.get(state_name, 'Invalid key!')

def convert_uf_to_state_name(uf):

    switcher = {
        "AC" : "Acre",				
        "AL" : "Alagoas",			
        "AM" : "Amazonas",			
        "AP" : "Amapá",				
        "BA" : "Bahia",				
        "CE" : "Ceará",				
        "DF" : "Distrito Federal",	
        "ES" : "Espírito Santo",	
        "GO" : "Goiás",				
        "MA" : "Maranhão",			
        "MG" : "Minas Gerais",		
        "MS" : "Mato Grosso do Sul",
        "MT" : "Mato Grosso",		
        "PA" : "Pará",				
        "PB" : "Paraíba",			
        "PE" : "Pernambuco",		
        "PI" : "Piauí",				
        "PR" : "Paraná",			
        "RJ" : "Rio de Janeiro",	
        "RN" : "Rio Grande do Norte",
        "RO" : "Rondônia",			
        "RR" : "Roraima",			
        "RS" : "Rio Grande do Sul",	
        "SC" : "Santa Catarina",	
        "SE" : "Sergipe",			
        "SP" : "São Paulo",			
        "TO" : "Tocantíns",			
    }

    return switcher.get(uf, 'Invalid key!')
    