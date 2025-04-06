from bs4 import BeautifulSoup
import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
tokenfile = open('token.txt', 'r')
tokenn = tokenfile.readline()
bot = Bot(tokenn) 
dp = Dispatcher()

dtb = open('database.txt', 'r')
readdtb = dtb.readlines()
readdtb_splitted = []
for x in readdtb:
    readdtb_splitted.append(x.split('context')[:1])

urll = 'https://www.avito.ru/sankt_peterburg_i_lo/noutbuki?cd=1&q=macbook&s=104'
request = requests.get(urll)

bs = BeautifulSoup(request.text, 'html.parser')

all_links = bs.find_all('a', rel="noopener", itemprop="url")

sorted_links = []

i = 0
i2 = 0
for link in all_links:
    if i2 == 2: break # Найти баланс между количеством обьявлений и кулдауном проверки
    if i == 1: 
        i = 0
        continue
    sorted_links.append('https://avito.ru' + link["href"])
    i += 1
    i2 += 1

sorted_links_splitted = []
for x in sorted_links:
    sorted_links_splitted.append(x.split('context')[:1])

if sorted(sorted_links_splitted) == sorted(readdtb_splitted):
    print('vsechetko')
else:
    print('Find new item!')
    with open('database.txt', 'w') as dtbw:
        for i in sorted_links:
            dtbw.write(f"{i}\n")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я бот для приветствия новых участников чата.")
    i = 0
    i2 = 0
    for link in all_links:
        if i2 == 10: break
        if i == 1:
            i = 0
            continue
        await message.answer('https://avito.ru' + link["href"])
        i += 1
        i2 += 1

async def main():
    await dp.start_polling(bot)

# asyncio.run(main())