from bs4 import BeautifulSoup
import requests
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from aiogram.types import InlineKeyboardMarkup, KeyboardButton, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

# Инициализация бота
tokenfile = open('token.txt', 'r')
tokenn = tokenfile.readline().strip()
bot = Bot(tokenn)
dp = Dispatcher()

chat_id = '-1002625392148'

# Хэндлер для команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет, братан! Я бот для парсинга Avito!")
    with open('database.txt', 'r') as dtb:
        links = dtb.readlines()
        for link in links[:10]:
            await message.answer(link.strip())


async def start_pars():
    while True:
        # Читаем существующие ссылки и режем их
        with open('database.txt', 'r') as dtb:
            readdtb = dtb.readlines()
            readdtb_splitted = [x.split('context')[0].strip() for x in readdtb if x.strip()]

        # Парсим Avito
        urll = 'https://www.avito.ru/sankt_peterburg_i_lo/noutbuki?cd=1&q=macbook&s=104'
        request = requests.get(urll)
        bs = BeautifulSoup(request.text, 'html.parser')
        all_links = bs.find_all('a', rel="noopener", itemprop="url")

        sorted_links = []
        i = 0
        i2 = 0
        for link in all_links:
            if i2 == 2: break
            if i == 1:
                i = 0
                continue
            sorted_links.append('https://avito.ru' + link["href"])
            i += 1
            i2 += 1

        # Режем новые ссылки так же, как старые
        sorted_links_splitted = [x.split('context')[0] for x in sorted_links]

        # Проверяем, есть ли новые объявления
        new_items = False
        new_link = ''
        for link in sorted_links_splitted:
            if link not in readdtb_splitted:
                new_items = True
                new_link = link
                break

        # Обновляем файл и выводим результат
        if new_items:
            with open('database.txt', 'w') as dtbw:
                for link in sorted_links:  # Пишем полные ссылки
                    dtbw.write(f"{link}\n")
            print('Найдено что-то новенькое!')
            await bot.send_message('-1002625392148', text=new_link)

        else:
            # await bot.send_message('-1002625392148', text='ss')
            print('Ничего пока не найдено, ожидаем...')

        await asyncio.sleep(10)  # Ждём 10 секунд

async def main():
    asyncio.create_task(start_pars())
    await dp.start_polling(bot)


asyncio.run(main())