
# Bike Theft Berlin Telegram Bot

This is a telegram that provides daily updated information about bike theft in Berlin.

## Screenshots

![Bildschirmfoto 2022-12-25 um 10 48 50 PM](https://user-images.githubusercontent.com/66785534/209482814-477d2c79-6215-4597-b427-808f881ee969.png)
![Bildschirmfoto 2022-12-25 um 10 48 58 PM](https://user-images.githubusercontent.com/66785534/209482820-725d35a7-450f-44ae-ac3a-b63e4ed9a634.png)
![Bildschirmfoto 2022-12-25 um 10 49 12 PM](https://user-images.githubusercontent.com/66785534/209482822-d59c845f-3ced-4482-aeea-d6d23385f86c.png)


## Model

A machine learning model (Gradient Boost Regressor) reads in all complaints filed with the Berlin Police and makes a predicition for the current day.
The features used for the prediction are year, month, day in month, weekday, holiday, temperature. The model is updated daily.

## Data Set

The Berlin Police provides a data set with all complaints for bicycle theft in Berlin from 1st January 2021.
The data is openly accessible here: https://daten.berlin.de/datensaetze/fahrraddiebstahl-berlin

## Telegram Bot

The telegram bot can be accessed here: https://t.me/RideSafeBerlin_bot
The daily updated analysis is made available through a telegram bot. The three main features are:
A daily report with the number of bikes predicted to be stolen on the current day. 
A risk assessment for the neighbourhood associated with the location sent via telegram. And some interesting facts about bike theft in Berlin.