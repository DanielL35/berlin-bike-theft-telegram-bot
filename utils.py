import pandas as pd
import datetime
import requests
import json
from datetime import date
import holidays
import geopandas as gpd
import random

# read the data
def read_data(path):

    df = pd.read_csv(path,
                     parse_dates=True,
                     encoding = "cp1252",
                     infer_datetime_format=True)

    # clean data   
    df['tocc'] = pd.to_datetime(df['ANGELEGT_AM'],
                                format="%d.%m.%Y")#,
                                # infer_datetime_format=True)

    df['toc_start'] = pd.to_datetime(df['TATZEIT_ANFANG_DATUM'],
                                     format="%d.%m.%Y") \
                    + pd.to_timedelta(df['TATZEIT_ANFANG_STUNDE'], unit='h')
                
    df['toc_end'] = pd.to_datetime(df['TATZEIT_ENDE_DATUM'],
                                     format="%d.%m.%Y") \
                    + pd.to_timedelta(df['TATZEIT_ENDE_STUNDE'], unit='h')

    df.rename(columns={
                       'SCHADENSHOEHE': 'damage',
                       'VERSUCH':'attempt',
                       'ART_DES_FAHRRADS':'bike_type',
                       'DELIKT':'delict',
                       'ERFASSUNGSGRUND':'crime',
            #           'ANGELEGT_AM':'registered'
                       },
                       inplace=True
             )

    df.drop(['TATZEIT_ANFANG_DATUM', 'TATZEIT_ANFANG_STUNDE',
             'TATZEIT_ENDE_DATUM', 'TATZEIT_ENDE_STUNDE', 'ANGELEGT_AM'],
             axis='columns',
             inplace=True
           )
    
    return df

# select a random point in crime time interval -> toc_rand
def set_random_time(df, column_start_time, column_end_time):
    '''Add a column with a random time between two timestamps.'''
    # create a column with the time delta
    df['toc_rand'] = df[column_end_time] - df[column_start_time]
    # select a random hour out of the time delta, i.e. 3 from 0-5
    df['toc_rand'] = df['toc_rand'].apply(
        lambda x: random.randint(0, x.seconds / (60*60))
        )
    # return the new time: start time + random hour from the time delta
    return df['toc_start'] + pd.to_timedelta(df['toc_rand'], unit='h')


def create_time_series(df):
    # apply the function to the df
    df['toc_rand'] = set_random_time(df, 'toc_start', 'toc_end')
    # create a new column with the date of the toc
    df['toc_rand_date'] = df['toc_rand'].apply(lambda x: x.date())
    # create the time series
    s = df.groupby(by='toc_rand_date').size()
    s = s.asfreq(freq = 'd', fill_value=0)
    return s

def get_weather_data(s):
    start_date = s.index.min().strftime("%Y-%m-%d")#'2021-01-01'  # use format yyyy-mm-dd
    # start_date_str = f'{df.index.min().year}-{df.index.min().month}
    end_date = s.index.max().strftime("%Y-%m-%d")#'2022-11-23'
    lat = 52.50083411524758
    lon = 13.402133467384548
    curl = f'https://api.brightsky.dev/weather?date={start_date}&last_date={end_date}&lat={lat}&lon={lon}&units=si'
    res = requests.get(curl)
    print(f'connecting to brightsky api. response: {res.status_code}')
    json = res.json()
    # create a data frame with T / pp / 
    timestamp, T = [], []
    for i in json['weather']:
        timestamp.append(i['timestamp'])
        T.append(i['temperature'])

    weather = pd.DataFrame({
                    'temperature':T,
                    'timestamp':pd.to_datetime(timestamp)}
                        )
    
    weather.set_index('timestamp',inplace=True)

    weather_resampled = pd.DataFrame({
                    'temperature':weather['temperature'].resample('1D').mean(),
                    })
    return weather_resampled


def merge_weather_data(df, weather_resampled):
    sjoin = pd.DataFrame({'thefts':df})
    df_final = sjoin.join(weather_resampled.tz_localize(None), how='left')
    return df_final


def add_datetime_features(df):
    """ take datetime information from index and add new columns """
    df['year'] = df.index.year
    df['month'] = df.index.month
    # df['week_in_year'] = df.index.isocalendar().week.astype('int')
    df['day_in_month'] = df.index.day
    df['weekday'] = df.index.day_of_week
    # df['hour_in_day'] = df.index.hour

    # fix bug in week count
    # df.loc[(df['month'] == 1) & (df['week_in_year'] == 52),
            # 'week_in_year'] = 0
    
    return df

def add_holiday_feat(df):
    '''
    01.01.2022 (Samstag): Neujahr
    08.03.2022 (Dienstag): Internationaler Frauentag - NOT INCLUDED!!!
    15.04.2022 (Freitag): Karfreitag
    18.04.2022 (Montag): Ostermontag
    01.05.2022 (Sonntag): Tag der Arbeit
    26.05.2022 (Donnerstag): Christi Himmelfahrt
    06.06.2022 (Montag): Pfingstmontag
    03.10.2022 (Montag): Tag der Deutschen Einheit
    25.12.2022 (Sonntag): 1. Weihnachtsfeiertag
    26.12.2022 (Montag): 2. Weihnachtsfeiertag

    '''
    year_min = df.index.min().year
    year_max = df.index.max().year
    de_holidays = holidays.Germany(years=[year_min, year_max])

    df['is_holiday'] = [int(date in de_holidays) for date in df.index]
    
    return df

def read_geo_data(path):
    # load shape data for LORs
    gdf = gpd.read_file(path)
    return gdf

def merge_geo_df(gdf, df):
    heatmap = pd.DataFrame(df.groupby(by='LOR').size(),
                       columns = ['thefts']).reset_index()
    heatmap['LOR'] = heatmap['LOR'].apply(lambda x: str(x))
    heatmap['LOR'] = heatmap['LOR'].apply(lambda x: f'0{x}'[-8:])
    # join thefts per lor to lor gdf
    gdf = gdf.rename(columns={'PLR_ID': 'LOR'})
    # join
    final = gdf.set_index('LOR').join(heatmap.set_index('LOR'))
    
    return final


