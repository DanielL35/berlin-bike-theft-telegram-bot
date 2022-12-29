nl = '\n'

start = f'Welcome! Send your location to get started!{nl}\
{nl}\
{nl}\
📊 /statistics{nl}\
🆕 /dailyReport{nl}\
💡 /about{nl}'

daily = {
    'part_1':f'The forecast today 💻🪄 {nl}',
    'very_bad_weather':'🌪💥🚲',
    'bad_weather':'⚡️⛈🚲',
    'okay_weather':'🌨🌦🚲',
    'nice_weather':'🌈🌤🚲',
    'part_2':' are predicted to be stolen across the city today.',
    'part_3':'The daily average for Berlin is ',
    'other_options':f'{nl}{nl} Click /statistics for bike theft statistics or /about for more info.'}

stats = {'intro':f'🧟🚲The five most popular neighbourhoods for bike thieves are:{nl}',
         "emoji1rst":'🥇',
         'emoji2nd':'🥈',
         'emoji3rd':'🥉',
         'emoji4th':'🏆',
         'emoji5th':'🏆',
         'worstday1':'📆 The worst day in bike theft history was',
         'worstday2':'when',
         'worstday3':'bikes were stolen in Berlin.',
         'bike_types': f'🚴‍🚴‍ The types of bikes are divided like this (since 01/01/2021):{nl}',
         'most_valuable_bikes':f'💵 The highest average damage per bike is found in:{nl}'
         }

risk = {
        'intro':f'Your risk level 🚲 {nl} {nl}',
        'risk_level_extreme':f'EXTREME RISK 💥 {nl}🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥 {nl} {nl}',
        'risk_message_extreme':'Be careful!',
        'risk_level_high':f' HIGH RISK 💣 {nl}🟥🟥🟥🟥🟥🟥🟥⬜️⬜️⬜️ {nl} {nl}',
        'risk_message_high':'Make sure to find a save spot!',
        'risk_level_medium':f' MEDIUM RISK 🌵 {nl}🟨🟨🟨🟨🟨⬜️⬜️⬜️⬜️⬜️ {nl} {nl}',
        'risk_message_medium':'All good!',
        'risk_level_low':f' LOW RISK 😌 {nl}🟩🟩🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️ {nl} {nl}',
        'risk_message_low':'All good!',
        'risk_level_very_low':f' VERY LOW RISK ☘️ {nl}🟩⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️⬜️ {nl} {nl}',
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