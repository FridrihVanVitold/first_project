import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

import keyboards

bot = Bot("7404984778:AAERkdcmadRi8oEJXMd9BgPS3KTOhgQ3Plk")
dp = Dispatcher()

smiles = [
    ["🥑", "Я люблю авокадо!"],
    ["🍓", "Клубника - это орех"],
    ["💭", "Ох.. как много идей!"],
    ["🙃", "У тебя всё получится!"]
]


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello, AIOgram 3.x", reply_markup=keyboards.main_kb)


@dp.callback_query(keyboards.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: keyboards.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0

    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len(smiles) - 1) else page_num

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"{smiles[page][0]} <b>{smiles[page][1]}</b>",
            reply_markup=keyboards.paginator(page)
        )
    await call.answer()


@dp.message(F.text.lower().in_(["хай", "хелоу", "привет"]))
async def greetings(message: Message):
    await message.reply("Приет!")


@dp.message()
async def echo(message: Message):
    msg = message.text.lower()

    if msg == "ссылки":
        await message.answer("Вот ваши ссылки:", reply_markup=keyboards.links_kb)
    elif msg == "спец. кнопки":
        await message.answer("Спец. кнопки:", reply_markup=keyboards.spec_kb)
    elif msg == "калькулятор":
        await message.answer("Введите выражение:", reply_markup=keyboards.calc_kb())
    elif msg == "смайлики":
        await message.answer(f"{smiles[0][0]} <b>{smiles[0][1]}</b>", reply_markup=keyboards.paginator())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=keyboards.main_kb)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())