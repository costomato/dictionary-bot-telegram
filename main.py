import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
import os
from dotenv import load_dotenv
from telegram.ext import *
import methods

load_dotenv()

PORT = int(os.getenv('PORT'))
TOKEN = os.getenv('BOT_TOKEN')

print("Starting bot...")

def start_command(update, context):
    update.message.reply_text("Hello there, I'm your handy dictionary. Send me any word for which you want to know the meaning.")

def help_command(update, context):
    update.message.reply_text("Send me any word and I will try to find the meaning for it.")

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

    if len(result) <= 4000:
        context.bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=result, parse_mode=ParseMode.MARKDOWN)
    else: # split the message if it's too long
        chunk_size = 4000
        while result:
            y = result[:chunk_size]
            if '\n' in y:
                j = y.rindex('\n')
                if msg:
                    context.bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=y[:j], parse_mode=ParseMode.MARKDOWN)
                    msg = None
                else:
                    context.bot.send_message(chat_id=chat_id, text=y[:j], parse_mode=ParseMode.MARKDOWN)
                result = result[j+1:]
            else:
                context.bot.send_message(chat_id=chat_id, text=y, parse_mode=ParseMode.MARKDOWN)
                result = result[chunk_size:]

def inline_query(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(InlineQueryResultArticle(
        id=query,
        title=query,
        input_message_content=InputTextMessageContent(methods.search_word(query)),
    ))
    context.bot.answer_inline_query(update.inline_query.id, results)

def error(update, context):
    # print(f'Update {update} caused error {context.error}')
    print('Update', update, 'caused error', context.error)
    update.message.reply_text("Something bad happened.")

if __name__ == '__main__':
    # updater = Updater(keys.bot_token, use_context=True)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    # handle messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # handle inline queries
    dp.add_handler(InlineQueryHandler(inline_query))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN, webhook_url=os.getenv('BASE_URL') + TOKEN)

    updater.idle()


'''
Bot commands:

start - Start the bot
help - Show help
'''
