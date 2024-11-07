import pandas as pd

def cargar_datos():
    """Carga los archivos CSV para cada año y devuelve los DataFrames."""
    data_2015 = pd.read_csv('data/2015.csv')
    data_2016 = pd.read_csv('data/2016.csv')
    data_2017 = pd.read_csv('data/2017.csv')
    data_2018 = pd.read_csv('data/2018.csv')
    data_2019 = pd.read_csv('data/2019.csv')
    return data_2015, data_2016, data_2017, data_2018, data_2019

def limpiar_datos(data_2015, data_2016, data_2017, data_2018, data_2019):
    """Realiza las operaciones de limpieza y estandarización en los DataFrames."""
    # Limpieza de 2015
    data_2015 = data_2015.drop(columns=['Region', 'Happiness Rank', 'Standard Error', 'Dystopia Residual'])
    data_2015 = data_2015.rename(columns={'Family': 'Social support'}).round(4)
    
    # Limpieza de 2016
    data_2016 = data_2016.drop(columns=['Region', 'Happiness Rank', 'Dystopia Residual', 'Lower Confidence Interval', 'Upper Confidence Interval'])
    data_2016 = data_2016.rename(columns={'Family': 'Social support'}).round(4)
    
    # Limpieza de 2017
    data_2017.columns = data_2017.columns.str.replace('"', '', regex=False).str.replace("'", "", regex=False)
    data_2017 = data_2017.drop(columns=['Happiness.Rank', 'Whisker.high', 'Whisker.low', 'Dystopia.Residual'])
    data_2017 = data_2017.rename(columns={
        'Happiness.Score': 'Happiness Score',
        'Economy..GDP.per.Capita.': 'Economy (GDP per Capita)',
        'Family': 'Social support',
        'Health..Life.Expectancy.': 'Health (Life Expectancy)',
        'Trust..Government.Corruption.': 'Trust (Government Corruption)'
    }).round(4)
    columnas_2017 = list(data_2017.columns)
    columnas_2017[6], columnas_2017[7] = columnas_2017[7], columnas_2017[6]
    data_2017 = data_2017[columnas_2017]
    
    # Limpieza de 2018
    data_2018 = data_2018.drop(columns=['Overall rank'])
    data_2018 = data_2018.rename(columns={
        'Score': 'Happiness Score',
        'GDP per capita': 'Economy (GDP per Capita)',
        'Healthy life expectancy': 'Health (Life Expectancy)',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust (Government Corruption)',
        'Country or region': 'Country'
    }).round(4)
    columnas_2018 = list(data_2018.columns)
    columnas_2018[6], columnas_2018[7] = columnas_2018[7], columnas_2018[6]
    data_2018 = data_2018[columnas_2018]
    
    # Limpieza de 2019
    data_2019 = data_2019.drop(columns=['Overall rank'])
    data_2019 = data_2019.rename(columns={
        'Score': 'Happiness Score',
        'GDP per capita': 'Economy (GDP per Capita)',
        'Healthy life expectancy': 'Health (Life Expectancy)',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust (Government Corruption)',
        'Country or region': 'Country'
    }).round(4)
    columnas_2019 = list(data_2019.columns)
    columnas_2019[7], columnas_2019[6] = columnas_2019[6], columnas_2019[7]
    data_2019 = data_2019[columnas_2019]
    
    # Agregar columna de año
    data_2015['Year'] = 2015
    data_2016['Year'] = 2016
    data_2017['Year'] = 2017
    data_2018['Year'] = 2018
    data_2019['Year'] = 2019
    
    # Combinar los datos
    data_combinada = pd.concat([data_2015, data_2016, data_2017, data_2018, data_2019], ignore_index=True)
    data_combinada = data_combinada.dropna()
    
    return data_combinada

def guardar_datos(data, path='data/Model_Data.csv'):
    """Guarda el DataFrame combinado en un archivo CSV."""
    data.to_csv(path, index=False)
    print(f"Archivos combinados exitosamente en '{path}' con {data.shape[0]} filas y {data.shape[1]} columnas")

# Uso de las funciones
data_2015, data_2016, data_2017, data_2018, data_2019 = cargar_datos()
data_limpia = limpiar_datos(data_2015, data_2016, data_2017, data_2018, data_2019)
guardar_datos(data_limpia)
