import pandas as pd

def load_data():
    """Loads the CSV files for each year and returns the DataFrames."""
    data_2015 = pd.read_csv('data/2015.csv')
    data_2016 = pd.read_csv('data/2016.csv')
    data_2017 = pd.read_csv('data/2017.csv')
    data_2018 = pd.read_csv('data/2018.csv')
    data_2019 = pd.read_csv('data/2019.csv')
    return data_2015, data_2016, data_2017, data_2018, data_2019

def clean_data(data_2015, data_2016, data_2017, data_2018, data_2019):
    """Performs cleaning and standardization operations on the DataFrames."""
    # Cleaning for 2015
    data_2015 = data_2015.drop(columns=['Region', 'Happiness Rank', 'Standard Error', 'Dystopia Residual'])
    data_2015 = data_2015.rename(columns={'Family': 'Social support'}).round(4)
    
    # Cleaning for 2016
    data_2016 = data_2016.drop(columns=['Region', 'Happiness Rank', 'Dystopia Residual', 'Lower Confidence Interval', 'Upper Confidence Interval'])
    data_2016 = data_2016.rename(columns={'Family': 'Social support'}).round(4)
    
    # Cleaning for 2017
    data_2017.columns = data_2017.columns.str.replace('"', '', regex=False).str.replace("'", "", regex=False)
    data_2017 = data_2017.drop(columns=['Happiness.Rank', 'Whisker.high', 'Whisker.low', 'Dystopia.Residual'])
    data_2017 = data_2017.rename(columns={
        'Happiness.Score': 'Happiness Score',
        'Economy..GDP.per.Capita.': 'Economy (GDP per Capita)',
        'Family': 'Social support',
        'Health..Life.Expectancy.': 'Health (Life Expectancy)',
        'Trust..Government.Corruption.': 'Trust (Government Corruption)'
    }).round(4)
    columns_2017 = list(data_2017.columns)
    columns_2017[6], columns_2017[7] = columns_2017[7], columns_2017[6]
    data_2017 = data_2017[columns_2017]
    
    # Cleaning for 2018
    data_2018 = data_2018.drop(columns=['Overall rank'])
    data_2018 = data_2018.rename(columns={
        'Score': 'Happiness Score',
        'GDP per capita': 'Economy (GDP per Capita)',
        'Healthy life expectancy': 'Health (Life Expectancy)',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust (Government Corruption)',
        'Country or region': 'Country'
    }).round(4)
    columns_2018 = list(data_2018.columns)
    columns_2018[6], columns_2018[7] = columns_2018[7], columns_2018[6]
    data_2018 = data_2018[columns_2018]
    
    # Cleaning for 2019
    data_2019 = data_2019.drop(columns=['Overall rank'])
    data_2019 = data_2019.rename(columns={
        'Score': 'Happiness Score',
        'GDP per capita': 'Economy (GDP per Capita)',
        'Healthy life expectancy': 'Health (Life Expectancy)',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust (Government Corruption)',
        'Country or region': 'Country'
    }).round(4)
    columns_2019 = list(data_2019.columns)
    columns_2019[7], columns_2019[6] = columns_2019[6], columns_2019[7]
    data_2019 = data_2019[columns_2019]
    
    # Add year column
    data_2015['Year'] = 2015
    data_2016['Year'] = 2016
    data_2017['Year'] = 2017
    data_2018['Year'] = 2018
    data_2019['Year'] = 2019
    
    # Combine the data
    combined_data = pd.concat([data_2015, data_2016, data_2017, data_2018, data_2019], ignore_index=True)
    combined_data = combined_data.dropna()
    
    return combined_data

def save_data(data, path='data/Model_Data.csv'):
    """Saves the combined DataFrame to a CSV file."""
    data.to_csv(path, index=False)
    print(f"Data successfully combined and saved to '{path}' with {data.shape[0]} rows and {data.shape[1]} columns")

# Using the functions
data_2015, data_2016, data_2017, data_2018, data_2019 = load_data()
cleaned_data = clean_data(data_2015, data_2016, data_2017, data_2018, data_2019)
save_data(cleaned_data)
