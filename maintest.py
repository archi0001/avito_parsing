from bs4 import BeautifulSoup
import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton


logging.basicConfig(level=logging.INFO)
tokenfile = open('/users/archi/documents/projects/avito/token.txt', 'r')
tokenn = tokenfile.readline()
bot = Bot(tokenn)  # Замените на ваш токен
dp = Dispatcher()

dtb = open('/users/archi/documents/projects/avito/database.txt', 'r')
readdtb = dtb.readlines()
# print(readdtb)

# dtbw = open('/users/archi/documents/projects/avito/database.txt', 'w')



urll = 'https://www.avito.ru/sankt_peterburg_i_lo/noutbuki?cd=1&q=macbook&s=104'
request = requests.get(urll)

bs = BeautifulSoup(request.text, 'html.parser')

all_links = bs.find_all('a', rel="noopener", itemprop="url")

sorted_links = []

i = 0
i2 = 0
for link in all_links:
    if i2 == 10: break
    if i == 1:
        i = 0
        continue
    sorted_links.append('https://avito.ru' + link["href"])
    i += 1
    i2 += 1

if sorted_links == readdtb:
    print('vsechetko')
else:
    with open('/users/archi/documents/projects/avito/database.txt', 'w') as dtbw:
        for i in sorted_links:
            print('sdfgh')
            dtbw.write(f"{i}\n")
# i = 0
# i2 = 0
# for link in all_links:
#     if i2 == 10: break
#     if i == 1:
#         i = 0
#         continue
#     print('https://avito.ru' + link["href"])
#     i += 1
#     i2 += 1

@dp.message(Command("start"))  # Используем фильтр Command для команды "/start"
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
        # print('https://avito.ru' + link["href"])
        i += 1
        i2 += 1

async def main():
    # Запуск polling
    await dp.start_polling(bot)


asyncio.run(main())