import telebot
import os
import re
from tiktok_downloader import services, InvalidUrl, info_post
from config import TOKEN

# передача токена
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Скопируй мне ссылку на видео из ТТ, и я тебе его перезалью.')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Копируешь в текстовое поле внизу ссылку из тиктока, если ссылка корректная, '
                                      'я скину видео. В зависимости от веса, видео может загружаться даже несколько минут'
                                      ', имей терпение. Когда пройдёт примерно 50% времени загрузки, я тебя уведомлю.')


@bot.message_handler()
def load_video(message):
    if message.text.startswith('https://www.tiktok.com') or re.search(r'https://v\w\.tiktok\.com*', message.text):
        url = message.text
        bot.send_message(message.chat.id, 'Ну-ка что там у тебя...')
        try:
            path = f"D:\python dump\{message.from_user.id}.mp4"
            #path = f"/home/tt_porter_bot/tt_porter_bot/python_dump/{message.from_user.id}.mp4"
            info_post.service(url)[0].download(path)
            if os.stat(path).st_size / (1024 * 1024) > 50.0:
                bot.send_message(message.chat.id, f'К сожалению, телеграм не разрешает ботам загружать файлы больше 50 Мб'
                                                  f', твой файл: {os.stat(path).st_size / (1024 * 1024)} Мб'
                                                  f'\nИзвини, что не смог помочь :('
                                                  f'\n\nВ будущем я обязательно научусь!')
            else:
                bot.send_message(message.chat.id, 'Ещё немного и видео загрузится!')
                video = open(path, 'rb')
                bot.send_video(message.chat.id, video)
                video.close()
            os.remove(path)
        except Exception as error:
            bot.send_message(message.chat.id, 'Возникла какая-то ошибка :(\nПроверь ссылку и попробуй ещё раз.\n')
            print(error)
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю :-(")


bot.polling(none_stop=True)

