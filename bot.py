import telegram

bot = telegram.Bot(token='')

# chat_id = bot.get_updates()[-1].message.chat_id

# bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)



# location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
# contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
# custom_keyboard = [[ location_keyboard, contact_keyboard ]]
# reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
# bot.send_message(chat_id=355055025, 
#                  text="Would you mind sharing your location and contact with me?", 
#                  reply_markup=reply_markup)




# updater.start_polling()
# updater.idle()
