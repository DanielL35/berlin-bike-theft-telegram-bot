from utils import merge_weather_data, create_time_series, read_data, read_geo_data, get_weather_data, add_datetime_features, add_holiday_feat
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import MinMaxScaler,OneHotEncoder
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.linear_model import Lasso,Ridge,ElasticNet
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import FunctionTransformer
import datetime
import glob
import os
import math
#%%

def train_model(df):
    '''
    Parameters
    ----------
    df : data frame from bike theft data set.

    Returns
    -------
    Saves model in /model directory.

    '''
    # create a time series 
    df = create_time_series(df)

    # cut off last N days to account for reporting delay
    N = 7
    df = df.iloc[:-N]

    # add weather data for each day
    weather_data = get_weather_data(df)

    df = merge_weather_data(df, weather_data)

    # expand features
    df = add_datetime_features(df)

    df = add_holiday_feat(df)

    df = df.reset_index(drop=True)

    X =  df.drop(labels = 'thefts', axis=1)
    # label / dependent variable
    y = df['thefts']
    # train test split
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)

    def create_cycl_features(df):
        df = df[['day_in_month', 'month']].copy()
        df['cycl_month'] = pd.DataFrame(df['month']).applymap(math.sin)
        df['cycl_day_in_month'] = pd.DataFrame(df['day_in_month']).applymap(math.sin)
        df.reset_index(drop=True, inplace=True)
        return df
    
    # create cyclical features for months and days
    cycl_pipeline = make_pipeline(
        FunctionTransformer(create_cycl_features, validate=False)
        )
    # create polynomial features
    polynom_pipeline = make_pipeline(
        PolynomialFeatures(interaction_only=True,
                           include_bias=False,
                           degree=3),
        MinMaxScaler()
        )
    # apply transformations on columns
    transformer = make_column_transformer(
        (cycl_pipeline, ['day_in_month', 'month']),  
        (polynom_pipeline, ['temperature']),    
        (OneHotEncoder(handle_unknown='ignore'), ['weekday', 'year']),
        ('passthrough', ['is_holiday'])
        )
    # choose static parameters
    params = {
              'max_depth': 2,
              'min_samples_leaf': 5,
              'min_samples_split': 2,
              # 'n_estimators': 100
              }
    # set up model pipeline
    model_pipeline = make_pipeline(
        transformer,
        GradientBoostingRegressor(**params)
        )
    # fit model without grid search (this seems to be necessary for gradient boosting?)
    model_pipeline.fit(Xtrain, ytrain)

    param_grid = {
        'gradientboostingregressor__subsample': [0.5, 0.7, 0.9],
        'gradientboostingregressor__n_estimators': [50, 100, 200],
        # 'gradientboostingregressor_learning_rate': [0.01, 0.02, 0.05]
        }

    cv = GridSearchCV(
        model_pipeline,
        param_grid,
        cv=10
        )
 
    cv.fit(Xtrain, ytrain)

    print(f'train score: {cv.score(Xtrain, ytrain)}')
    print(f'test score: {cv.score(Xtest, ytest)}')
    
    return cv
    # # save model
    # now = datetime.datetime.now()
    # filename = f'model/{now.strftime("%Y_%m_%d_%H_%M")}_model.pkl'
    # with open(filename, 'wb') as f:
    #     pickle.dump(cv, f)
    
    # print(f'model saved as {filename}')
    
    # return


#%%

def get_daily_data(m, df, final):
    '''
    Create a dictionary that includes all statistics for the messages.

    '''
    # generate input for model
    df_today = pd.DataFrame(index = pd.Series(pd.to_datetime('today').normalize()))
    df_today = get_weather_data(df_today)
    df_today.set_index(df_today.index.tz_localize(None), inplace=True)
    df_today = add_datetime_features(df_today)
    df_today = add_holiday_feat(df_today)
    df_today = df_today.reset_index(drop=True)

    # calculate thefts per LOR overall and in last 7 days
    df['LOR'] = df['LOR'].apply(lambda x: str(x))
    df['LOR'] = df['LOR'].apply(lambda x: f'0{x}'[-8:])

    all_thefts = pd.DataFrame(df.groupby(by='LOR').size(),
                       columns = ['thefts']).reset_index()
    all_thefts.set_index('LOR', inplace=True)
    all_thefts = pd.DataFrame(final['PLR_NAME']).join(all_thefts)
    all_thefts['thefts'].fillna(0, inplace=True)

    last_week = df['toc_end'] > pd.to_datetime('today').normalize() - pd.to_timedelta(14, unit='d')
    weekly_thefts = pd.DataFrame(df[last_week].groupby(by='LOR').size(),
                       columns = ['thefts']).reset_index()
    weekly_thefts.set_index('LOR', inplace=True)
    weekly_thefts = pd.DataFrame(final['PLR_NAME']).join(weekly_thefts)
    weekly_thefts['thefts'].fillna(0, inplace=True)


    lor_quantiles = [all_thefts['thefts'].quantile(0.2),
                     all_thefts['thefts'].quantile(0.4),
                     all_thefts['thefts'].quantile(0.6),
                     all_thefts['thefts'].quantile(0.8)
                     ]
        
    s = create_time_series(df)

    # cut off last N days to account for reporting delay
    N = 7
    s = s.iloc[:-N]
    
    daily_mean = round(s.mean())
    
    s_quantiles = [s.quantile(0.25),
                   s.quantile(0.5),
                   s.quantile(0.75)
                   ]
    
    daily_data = {
        'pred_thefts_all_Berlin':round(m.predict(df_today)[0]),
        'weekly_thefts_lor':weekly_thefts,
        'all_thefts_lor':all_thefts,
        'lor_quantiles':lor_quantiles,
        's_quantiles':s_quantiles,
        'daily_mean':daily_mean,
        's':s
        }

    return daily_data