import logging
import os
from datetime import timedelta

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from timeloop import Timeloop


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
API_KEY = os.environ['TELEGRAM_STOCK_API']
telegram_bot = telegram.Bot(API_KEY)
tl = Timeloop()


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: telegram.Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: telegram.Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def status_command(update: telegram.Update, context: CallbackContext) -> None:
    sendMessage("test")


def echo(update: telegram.Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text("doesn't work for you:(")
    print(update.message.chat_id)


@tl.job(interval=timedelta(seconds=60 * 60 * 24))
def sendStatus():
    sendMessage("test")


def sendMessage(msg):
    chat_id = int(os.environ['TELEGRAM_PERSONAL_CHAT_ID'])
    telegram_bot.send_message(chat_id, text=msg, disable_web_page_preview=True)


def main():
    init_telegram_bot()


def init_telegram_bot():
    tl.start()
    # sendMessage("telegram-bot started")
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(API_KEY)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


def kill_telegram_bot():
    tl.stop()


if __name__ == '__main__':
    main()
