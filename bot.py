# import logging
# import telegram
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id,
#                      text="I'm a bot, please talk to me!")

# def echo(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


# logging.basicConfig(format='%(asctime)s - %(name)s -%(levelname)s - %(messge)s',
#                     level=logging.INFO)

# updater = Updater(token='')
# dispatcher = updater.dispatcher

# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# # echo_handler = MessageHandler(Filters.text, echo)
# # dispatcher.add_handler(echo_handler)


# def caps(bot, update, args):
#      text_caps = ' '.join(args).upper()
#      bot.send_message(chat_id=update.message.chat_id, text=text_caps)

# caps_handler = CommandHandler('caps', caps, pass_args=True)
# dispatcher.add_handler(caps_handler)


# from telegram import InlineQueryResultArticle, InputTextMessageContent
# def inline_caps(bot, update):
#      query = update.inline_query.query
#      if not query:
#          return
#      results = list()
#      results.append(
#          InlineQueryResultArticle(
#              id=query.upper(),
#              title='Caps',
#              input_message_content=InputTextMessageContent(query.upper())
#          )
#      )
#      bot.answer_inline_query(update.inline_query.id, results)

# from telegram.ext import InlineQueryHandler
# inline_caps_handler = InlineQueryHandler(inline_caps)
# dispatcher.add_handler(inline_caps_handler)




# updater.start_polling()
# updater.idle()
