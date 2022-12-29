from text_data import replies
import pandas as pd

# get text data for the /start command
def get_start_msg():
    return replies['start']
# get text data for the /about command
def get_about_msg():
    return replies['about']
# get the text data for /statistics command
def get_stats_msg(daily_data, df):
    # add a new line for the f-strings
    nl = '\n'
    # first sentence in message
    intro = replies['stats']['intro']
    # get the five neighbourhoods with the highest number of registered stolen bikes
    top5 = daily_data['all_thefts_lor'].sort_values(by=['thefts'], ascending=False).head(5)
    rank_1 = f'{replies["stats"]["emoji1rst"]} {top5["PLR_NAME"][0]} : {top5["thefts"][0]} bikes {nl}'
    rank_2 = f'{replies["stats"]["emoji2nd"]} {top5["PLR_NAME"][1]} : {top5["thefts"][1]} bikes {nl}'
    rank_3 = f'{replies["stats"]["emoji3rd"]} {top5["PLR_NAME"][2]} : {top5["thefts"][2]} bikes {nl}'
    rank_4 = f'{replies["stats"]["emoji4th"]} {top5["PLR_NAME"][3]} : {top5["thefts"][3]} bikes {nl}'
    rank_5 = f'{replies["stats"]["emoji5th"]} {top5["PLR_NAME"][4]} : {top5["thefts"][4]} bikes {nl}'
    ranks = f'{intro}{rank_1}{rank_2}{rank_3}{rank_4}{rank_5}'
    # find the day with thehighest number of bike thefts
    day = daily_data['s'].idxmax().strftime("%d/%m/%Y")
    number = daily_data['s'].max()
    worst_day = f'{replies["stats"]["worstday1"]} ' + f'{day}' + f' {replies["stats"]["worstday2"]} '  f'{number} ' + f'{replies["stats"]["worstday3"]}'
    # group all bike thefts by the type of bike
    bike_types = pd.DataFrame(df.groupby(by='bike_type').size())
    bike_types['ger_type'] = bike_types.index
    # as the bike types are in German they need to be translated
    bike_types['en_type'] = bike_types['ger_type'].replace({
                                                            'Damenfahrrad':'''Ladies bike''',
                                                            'Fahrrad':'unspecified',
                                                            'Herrenfahrrad':'''Men's bike''',
                                                            'Kinderfahrrad':'''Children's bike''',
                                                            'Lastenfahrrad':'Cargo bike',
                                                            'Mountainbike':'Mountain bike',
                                                            'Rennrad':'Racing bike',
                                                            'diverse Fahrräder':'Several bikes'
                                                          })
    bike_types = bike_types.sort_values(by=0, ascending=False)
    bike_types_msg = replies["stats"]["bike_types"]
    for index, row in bike_types.iterrows():
        bike_types_msg = f'{bike_types_msg}{row["en_type"]}: {row[0]}{nl}'
    # print the neighbourhoods with the highest average damage
    damage = pd.DataFrame(df.groupby(by=['LOR']).agg({'crime':'count', 'damage':'mean'}))
    damage = damage[damage['crime'] > 20].sort_values(by='damage', ascending=False)
    most_valuable_bikes = replies["stats"]["most_valuable_bikes"]
    for index, row in damage.head(3).iterrows():
        n = daily_data['all_thefts_lor'][daily_data['all_thefts_lor'].index == index]['PLR_NAME'][0]
        d = round(row['damage'])
        most_valuable_bikes = f'{most_valuable_bikes}{n}: {d}€{nl}'
        
    # put everything in one string
    return f'{ranks}{nl}{worst_day}{nl}{nl}{bike_types_msg}{nl}{most_valuable_bikes}'

def get_risk_msg(your_loc, thefts_lor, daily_data):
    nl = '\n'
    intro = replies["risk"]["intro"]

    if thefts_lor > daily_data['lor_quantiles'][3]:
        risk_level = replies["risk"]['risk_level_extreme']
        risk_message = replies["risk"]['risk_message_extreme']
    elif thefts_lor > daily_data['lor_quantiles'][2]:
        risk_level = replies["risk"]['risk_level_high'] 
        risk_message = replies["risk"]['risk_message_high'] 
    elif thefts_lor > daily_data['lor_quantiles'][1]:
        risk_level = replies["risk"]['risk_level_medium'] 
        risk_message = replies["risk"]['risk_message_medium'] 
    elif thefts_lor > daily_data['lor_quantiles'][0]:
        risk_level = replies["risk"]['risk_level_low'] 
        risk_message = replies["risk"]['risk_message_low'] 
    else:
        risk_level = replies["risk"]['risk_level_very_low'] 
        risk_message = replies["risk"]['risk_message_very_low'] 

    # message = f'You are currently located in {your_loc}. This is a{risk_level} neighbourhood. {risk_message}'
    mask = daily_data['weekly_thefts_lor']['PLR_NAME'] == your_loc
    thefts_last_week = int(daily_data['weekly_thefts_lor'][mask]['thefts'][0])

    if thefts_last_week == 1:
        grammar_helper = replies["risk"]['grammar_helper_sing'] 
    else:
        grammar_helper = replies["risk"]['grammar_helper_plur'] 

    theft_count_lor = f'{thefts_last_week} {grammar_helper} {replies["risk"]["last"]}'

    loc_msg = f'You are currently in {your_loc}. {risk_message} {nl}{theft_count_lor} {nl}'

    message = intro + '\n' + risk_level + loc_msg

    return message

def get_daily_msg(daily_data):
    nl = '\n'
    
    part_1 = replies['daily']['part_1']
    
    if daily_data['pred_thefts_all_Berlin'] > daily_data['s_quantiles'][2]:
        cond_emoji = replies['daily']['very_bad_weather']
    elif daily_data['pred_thefts_all_Berlin'] > daily_data['s_quantiles'][1]:
        cond_emoji = replies['daily']['bad_weather']
    elif daily_data['pred_thefts_all_Berlin'] > daily_data['s_quantiles'][0]:
        cond_emoji = replies['daily']['okay_weather']
    else:
        cond_emoji = replies['daily']['nice_weather']
        
    predicted_today = daily_data['pred_thefts_all_Berlin']
    part_2 = str(predicted_today) + replies['daily']['part_2']
    
    mean_thefts = daily_data['daily_mean']
    part_3 = replies['daily']['part_3'] + str(mean_thefts)
    
    other_options = replies['daily']['other_options']
    
    msg = part_1 + f'{nl}' + part_2 + f'{nl}' + part_3 + f'{nl}' + f'{nl}' + cond_emoji + other_options
    
    return msg

def get_options_msg():
    return replies['options']