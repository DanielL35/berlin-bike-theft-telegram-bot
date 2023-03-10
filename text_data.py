nl = '\n'

start = f'Welcome! Send your location to get started!{nl}\
{nl}\
{nl}\
π /statistics{nl}\
π /dailyReport{nl}\
π‘ /about{nl}'

daily = {
    'part_1':f'The forecast today π»πͺ {nl}',
    'very_bad_weather':'πͺπ₯π²',
    'bad_weather':'β‘οΈβπ²',
    'okay_weather':'π¨π¦π²',
    'nice_weather':'ππ€π²',
    'part_2':' are predicted to be stolen across the city today.',
    'part_3':'The daily average for Berlin is ',
    'other_options':f'{nl}{nl} Click /statistics for bike theft statistics or /about for more info.'}

stats = {'intro':f'π§π²The five most popular neighbourhoods for bike thieves are:{nl}',
         "emoji1rst":'π₯',
         'emoji2nd':'π₯',
         'emoji3rd':'π₯',
         'emoji4th':'π',
         'emoji5th':'π',
         'worstday1':'π The worst day in bike theft history was',
         'worstday2':'when',
         'worstday3':'bikes were stolen in Berlin.',
         'bike_types': f'π΄βπ΄β The types of bikes are divided like this (since 01/01/2021):{nl}',
         'most_valuable_bikes':f'π΅ The highest average damage per bike is found in:{nl}'
         }

risk = {
        'intro':f'Your risk level π² {nl} {nl}',
        'risk_level_extreme':f'EXTREME RISK π₯ {nl}π₯π₯π₯π₯π₯π₯π₯π₯π₯π₯ {nl} {nl}',
        'risk_message_extreme':'Be careful!',
        'risk_level_high':f' HIGH RISK π£ {nl}π₯π₯π₯π₯π₯π₯π₯β¬οΈβ¬οΈβ¬οΈ {nl} {nl}',
        'risk_message_high':'Make sure to find a save spot!',
        'risk_level_medium':f' MEDIUM RISK π΅ {nl}π¨π¨π¨π¨π¨β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈ {nl} {nl}',
        'risk_message_medium':'All good!',
        'risk_level_low':f' LOW RISK π {nl}π©π©π©β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈ {nl} {nl}',
        'risk_message_low':'All good!',
        'risk_level_very_low':f' VERY LOW RISK βοΈ {nl}π©β¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈβ¬οΈ {nl} {nl}',
        'risk_message_very_low':'No worries!',
        'grammar_helper_sing':'bike was',
        'grammar_helper_plur':'bikes were',
        'last':f'registered stolen in this neighbourhood in the last two weeks.{nl}'
        
        
        }

about = 'Click here for more info on \
the methodology and the data set: https://github.com/DanielL35'

options = 'Invalid command! Click /statistics for bike theft\
statistics, /dailyReport or /about for more info'

replies = {
    'start':start,
    'about':about,
    'stats':stats,
    'risk':risk,
    'daily':daily,
    'options':options
    }