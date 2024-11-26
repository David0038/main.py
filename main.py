import telebot
import requests
import json

bot = telebot.TeleBot('7396486968:AAGupUYQjgwGdzwBSgVEMYi7rAbhXEBzwnk')
API = 'e9ed9cc83a633d513fc8fd7acbd2a24b'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, рад тебя видеть! Напиши название города!')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')

    if res.status_code == 200:
        data = json.loads(res.text)
        current_temp = round(data['main']['temp'])
        min_temp = round(data['main']['temp_min'])
        max_temp = round(data['main']['temp_max'])
        weather_condition = data['weather'][0]['main'].lower()

        if 'rain' in weather_condition:
            photo_path = 'Дождь_2024-11-07_19-50-28.jpg'
        elif 'thunderstorm' in weather_condition:
            photo_path = 'Местами грозы_2024-11-07_19-50-31.jpg'
        elif 'clouds' in weather_condition:
            photo_path = 'Облачно_2024-11-07_19-50-33.jpg' if current_temp > 0 else 'Пасмурно_2024-11-07_19-50-30.jpg'
        elif 'snow' in weather_condition:
            photo_path = 'Снег_2024-11-07_19-50-34.jpg'
        else:
            photo_path = 'Ясно_2024-11-07_19-50-29.jpg'

        with open(photo_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo,
                           caption=f'Погода в {city.capitalize()}:\n'
                                   f'🔺 Максимальная температура: {max_temp}°C\n'
                                   f'🌡 Текущая температура: {current_temp}°C\n'
                                   f'🔻 Минимальная температура: {min_temp}°C')

    else:
        bot.reply_to(message, 'Город указан неверно или не найден! Попробуйте ввести название города на английском или добавьте код страны.')


bot.polling(non_stop=True)

