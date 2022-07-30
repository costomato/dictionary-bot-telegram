import requests
from telegram import ParseMode
import os
from dotenv import load_dotenv
from telegram.ext import *
import keys

load_dotenv()

print("Starting bot...")

def start_command(update, context):
    update.message.reply_text("Hello there, I'm your handy dictionary. Send me any word for which you want to know the meaning.")

def help_command(update, context):
    # TODO
    update.message.reply_text("Send my any word and I will try to find the meaning for it.")

def custom_command(update, context):
    update.message.reply_text("Hello there, I'm your handy dictionary.")

def handle_message(update, context):
    msg = update.message.reply_text('One moment please...')
    chat_id = update.message.chat_id

    url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    data = requests.get(url + update.message.text).json()

    if type(data) is not list:
        context.bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text='Oops, I did not find any meaning for that word.')
        return

    result = ''
    count = 1
    for i in data:
        result += str(count) + '. *' + i['word'] + '*\n'
        if 'phonetic' in i:
            result += i['phonetic'] + '\n\n'
        for j in i['meanings']:
            if 'partOfSpeech' in j:
                result += '_' + j['partOfSpeech'] + '_\n'
            for k in j['definitions']:
                result += '-> ' + k['definition'] + '\n'
                if 'synonyms' in k and k['synonyms']:
                    result += '`Synonyms: ' + ', '.join(k['synonyms']) + '`\n'
                if 'antonyms' in k and k['antonyms']:
                    result += '`Antonyms: ' + ', '.join(k['antonyms']) + '`\n'
                if 'example' in k and k['example']:
                    result += '`Example: ' + k['example'] + '`\n'
            result += '\n'
        result += '\n'
        count += 1

    context.bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=result, parse_mode=ParseMode.MARKDOWN)
    

def error(update, context):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    # updater = Updater(keys.bot_token, use_context=True)
    updater = Updater(os.getenv('BOT_TOKEN'), use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))

    # handle messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


'''
Bot commands:

start - Start the bot
help - Show help
custom - Show custom message
'''