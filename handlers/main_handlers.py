import random
import os.path
from misc import bot
from shared import google_request

@bot.message_handler(commands=['start'])
def send_welcome(message):
  user = message.from_user
  user_name = user.first_name
  if user_name == None:
    user_name = '@{0}'.format(user.username)
  if user_name == None:
    user_name = 'человек'
  bot.send_message(message.chat.id,
    'Привет, {0.first_name}!\nМеня зовут <b>{1.first_name}</b> - <i>бот, у которого есть реальная работа</i>.'
      .format(message.from_user, bot.get_me()),
    parse_mode='html'
  )
  help(message)

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id,
    '<b>Вот, что я умею:</b>\n<i> - ничего</i>',
    parse_mode='html'
  )

@bot.message_handler(content_types=['new_chat_members'])
def handler_new_member(message):
  jsonD = message.json
  user_name = jsonD.get('new_chat_member').get('first_name')
  bot.send_message(
    message.chat.id, 'Добро пожаловать, <b>{0}</b>!\nРассказывай - кто ты, откуда, на чем сидишь, что за проект, как относишься к котам?'
      .format(user_name),
    parse_mode='html'
  )
  send_sticker(message)

@bot.message_handler(commands=['загугли'])
def send_google_resp(message):
  bot_action(message)
  req = message.text.lower().replace('/загугли', '').replace('кто', '').replace('такой', '').replace('что', '').replace('такое', '').strip()
  try:
    resp = google_request.googleRequest.find(req)
  except:
    resp = 'Проблемы с доступом к джойказино...'
    send_sticker(message, 'stickers/google_fail_01.tgs')
  bot.send_message(message.chat.id, '<i>{0}</i>'.format(resp), parse_mode='html')

@bot.message_handler(commands=['стикер', 'sticker'])
def send_sticker(message, path='stickers/hello_01.tgs'):
  sticker = open(path, 'rb')
  bot.send_sticker(message.chat.id, sticker)

@bot.message_handler(commands=['пикча', 'фото', 'картинка', 'изображение', 'img', 'image', 'picture'])
def send_image(message, num=-1):
  bot_action(message)
  images_path = 'images'
  num_files = sum(os.path.isfile(os.path.join(images_path, f)) for f in os.listdir(images_path))
  if num < 0 or num >= num_files:
    try: num = int(message.text.replace('/пикча', '').strip())
    except: num = -1
  if num < 0 or num >= num_files:
    num = random.randint(0, num_files - 1)
  try:
    img = open('images/cat_{0}.jpg'.format(num), 'rb')
    bot.send_photo(message.chat.id, img)
    img.close()
  except:
    resp = 'Не вышло...'
    bot.send_message(message.chat.id, '<i>{0}</i>'.format(resp), parse_mode='html')

@bot.message_handler(commands=['видео'])
def send_video(message):
  req = message.text.replace('/видео', '').strip()
  # TODO:
  bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=lkQ0LDx9jHs')

@bot.message_handler(commands=['звук', 'голос', 'аудио', 'sound', 'audio'])
def send_audio(message, path='audio/modem.mp3'):
  try:
    with open(path, 'rb') as f:
      audio = f.read()
      bot.send_audio(message.chat.id, audio)
  except:
    bot.send_message(message.chat.id, 'пиип... пииип...')

@bot.message_handler(commands=['умри', 'kill'])
def kill_bot(message):
  bot.send_message(message.chat.id, 'Этот мир жесток. Умираю.\n*умер*')
  send_sticker(message, 'stickers/strange_01.tgs')
  raise IOError("Вызвана смерть бота.")

@bot.message_handler()
def handler_message(message):
  bot_name = bot.get_me().first_name
  if bot_name.lower() in message.text.lower():
    response = message.text.replace(bot_name, '')
    bot.send_message(message.chat.id, response)

def bot_action(message, action='typing'):
  bot.send_chat_action(message.chat.id, action)