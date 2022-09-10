from os import getenv
from dotenv import load_dotenv
from telethon import TelegramClient
import redis
import os


API_ID= int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
REDIS_ENDPOINT = os.environ.get('REDIS_ENDPOINT').split(':')
REDIS_PASS = os.environ.get('REDIS_PASS')

REDIS = redis.Redis(
  host=REDIS_ENDPOINT[0],
  port=int(REDIS_ENDPOINT[1]),
  password=REDIS_PASS,
  )
  
try:
  REDIS.ping()
  print('Redis Alive!')
except Exception as e:
  print(e)
  
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
