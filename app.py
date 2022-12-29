import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from messages import get_start_msg, get_about_msg, get_stats_msg, get_risk_msg, get_options_msg, get_daily_msg
from utils import read_data, read_geo_data, merge_geo_df
from dotenv import load_dotenv
from model import train_model, get_daily_data
from risk import assess_location
#
load_dotenv()
# get environment variables
PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ.get('TOKEN')
URL = os.environ.get('URL')
GEO_DATA_PATH = os.environ.get('GEO_DATA_PATH')

RUN_LOCAL = True

BIKE_THEFT_DATA = read_data(URL)
GEO_DATA = read_geo_data(GEO_DATA_PATH)
FINAL = merge_geo_df(GEO_DATA, BIKE_THEFT_DATA)

def get_daily_report(df, final):
    m = train_model(df)
    daily_data = get_daily_data(m, df, final)
    daily_report = get_daily_msg(daily_data)
    return daily_data, daily_report

DAILY_DATA, DAILY_REPORT = get_daily_report(BIKE_THEFT_DATA, FINAL)
#%%
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    msg = get_start_msg()
    update.message.reply_text(msg)
    logger.warning('Update "%s" hit /start ', update)
    
def dailyReport(update, context):
    """Show more info on the project."""
    msg = DAILY_REPORT
    update.message.reply_text(msg)
    logger.warning('Update "%s" hit /dailyReport ', update)
    
def stats(update, context):
    """Show statistics."""
    msg = get_stats_msg(DAILY_DATA, BIKE_THEFT_DATA)
    update.message.reply_text(msg)
    logger.warning('Update "%s" hit /stats ', update)
    
def risk(update, context):
    """Show the risk assessment"""
    msg_in = update.message
    x = msg_in.location.longitude
    y = msg_in.location.latitude
    your_loc, thefts_lor = assess_location(x, y, FINAL)
    if your_loc is None:
        msg = 'Oh! 🐻 This location does not seem to be in Berlin. Try again!'
    else:
        msg = get_risk_msg(your_loc, thefts_lor, DAILY_DATA)
    update.message.reply_text(msg)
    logger.warning('Update "%s" hit /risk ', update)
    
def about(update, context):
    """Show more info on the project."""
    msg = get_about_msg()
    update.message.reply_text(msg)
    logger.warning('Update "%s" hit /about ', update)

def options(update, context):
    """Tell the user the command is invalid"""
    msg = get_options_msg()
    update.message.reply_text(msg)
    logger.warning('Update "%s" hit /options ', update)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("dailyReport", dailyReport))
    
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("statistics", stats))
        
    # on location get the geo coordinates
    dp.add_handler(MessageHandler(Filters.location,
                              risk,
                              pass_user_data=True))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("about", about))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, options))
   
    # log all errors
    dp.add_error_handler(error)
   
    if RUN_LOCAL:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url='https://telbot-polling.onrender.com/' + TOKEN)
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()