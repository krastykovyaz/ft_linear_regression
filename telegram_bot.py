import telebot, pickle

TELEGRAM_TOKEN = '*'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_price(theta0, theta1, mileage):
        return theta0 + theta1 * mileage

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    if message.text == '/start' or message.text == '/go':
        bot.send_message(message.chat.id, "Введите размер пробега в километрах...")
    else:
        try:
            with open('data.pickle', 'rb') as f:
                coefficients = pickle.load(f)
        except Exception as er:
            print(er)
        try:
            prices = get_price(coefficients['theta0'], coefficients['theta1'], float(message.text))
            prices = round(prices, 2)
            bot.send_message(message.chat.id, f'''Цена такой тачки {prices}''')
        except Exception as er:
            print(er)
            bot.send_message(message.chat.id, "Введите размер пробега в километрах корректно!")
        
        
        
bot.polling(none_stop=True)  
