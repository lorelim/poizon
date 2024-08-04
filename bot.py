import asyncio
import logging
import sys

from aiogram import types
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from assets.config import TOKEN_
from aiogram.enums import ParseMode
from aiogram import F
from assets import config
from assets.sqlighter import SQLighter
from assets import funcs
from aiogram.methods.send_photo import SendPhoto
from aiogram.types import InputFile, BufferedInputFile
from assets import keyboards
from aiogram.client.session.aiohttp import AiohttpSession


TOKEN = TOKEN_


dp = Dispatcher()

bot = Bot(token=TOKEN)

sql = SQLighter("assets/database/data.db")


async def delete_message(chat_id, message):
    pr_msg = sql.get_pr_msg(message.from_user.id)

    await bot.delete_message(message.from_user.id, pr_msg)

@dp.message(F.text == "/admin")
async def admin(message: Message):

    if message.from_user.id == config.admin_id:

        sql.change_admin(message.from_user.id, True)
        await bot.send_message(message.from_user.id, "admin panel")

    else:
        await bot.send_message(message.from_user.id, "Ошибка")


@dp.message(F.text != "/start")
async def admin_cur(message: Message):

    if sql.check_admin(message.from_user.id):

        if message.text.split(":")[0] == "CNY" and len(message.text.split(":")) == 2:
            sql.change_cur("CNY", float(message.text.split(":")[1]))
            
        if message.text.split(":")[0] == "RUB" and len(message.text.split(":")) == 2:
            sql.change_cur("RUB", float(message.text.split(":")[1]))
            
        if message.text.split(":")[0] == "BYN" and len(message.text.split(":")) == 2:
            sql.change_cur("BYN", float(message.text.split(":")[1]))

        if message.text == "show":
            await bot.send_message(message.from_user.id, "CNY: " + str(sql.get_cur("CNY")) + "\n" +"RUB: " + str(sql.get_cur("RUB"))+ "\n" + "BYN: " + str(sql.get_cur("BYN")))
            
        if message.text == "leave":
            sql.change_admin(message.from_user.id, 0)
            await bot.send_message(message.from_user.id, "leave admin panel")

    if (sql.get_state(message.from_user.id)):

        cny = int(message.text)

        usdt = funcs.calculator(cny, sql.get_cl_type(message.from_user.id), sql.get_cur("CNY"))  

        byn = usdt * sql.get_cur("BYN")
        rub = usdt * sql.get_cur("RUB")
            
        msg = await bot.send_message(message.from_user.id, "Итоговая цена в USDT: " + str(format(usdt, ".0f") + "\n" + "Итоговая цена в BYN: " + str(format(byn + byn * 0.05, ".0f")) + "\n" + "Итоговая цена в RUB: " + str(format(rub + rub * 0.05, ".0f"))), reply_markup = keyboards.kb_order_product)

        sql.change_state(message.from_user.id, False)

            

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    if sql.check_user(message.from_user.id) == True:

        with open(config.main_photo, "rb") as photo_file:
            photo_bytes = photo_file.read()

        photo = BufferedInputFile(photo_bytes, config.main_photo)

        msg = await bot(SendPhoto(
            chat_id = message.from_user.id,
            photo = photo, 
            caption = config.start_message,
            reply_markup = keyboards.kb_main,
            ))

        if (sql.get_pr_msg(message.from_user.id) != 0):
            await delete_message(message.from_user.id, message)

        sql.change_msg(message.from_user.id, msg.message_id)

    else:

        with open(config.main_photo, "rb") as photo_file:
            photo_bytes = photo_file.read()

        photo = BufferedInputFile(photo_bytes, config.main_photo)

        msg = await bot(SendPhoto(
            chat_id = message.from_user.id,
            photo = photo, 
            caption = config.start_message,
            reply_markup = keyboards.kb_main,
            ))
        sql.add_user(message.from_user.id, msg.message_id)

        sql.change_msg(message.from_user.id, msg.message_id)



@dp.callback_query(lambda c:c.data.startswith("main"))
async def handle_main(callback_query: types.CallbackQuery):

    if callback_query.data.endswith("1"):

        if (sql.get_pr_msg(callback_query.from_user.id) != 0):
            await delete_message(callback_query.from_user.id, callback_query)

        msg = await bot.send_message(callback_query.from_user.id, config.calculator_message, reply_markup = keyboards.kb_calc)

        sql.change_msg(callback_query.from_user.id, msg.message_id)


@dp.callback_query(lambda c:c.data.startswith("calc"))
async def handle_calc(callback_query: types.CallbackQuery):
    
    sql.change_cl_type(callback_query.from_user.id, int(callback_query.data[-1]))
    sql.change_state(callback_query.from_user.id, True)

    if (sql.get_pr_msg(callback_query.from_user.id) != 0):
        await delete_message(callback_query.from_user.id, callback_query)

    msg = await bot.send_message(callback_query.from_user.id, config.order_message)

    sql.change_msg(callback_query.from_user.id, msg.message_id)

    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "menu")
async def back_to_menu(callback_query: types.CallbackQuery):

    with open(config.main_photo, "rb") as photo_file:
            photo_bytes = photo_file.read()

    photo = BufferedInputFile(photo_bytes, config.main_photo)

    msg = await bot(SendPhoto(
        chat_id = callback_query.from_user.id,
        photo = photo, 
        caption = config.start_message,
        reply_markup = keyboards.kb_main,
        ))
    
    if (sql.get_pr_msg(callback_query.from_user.id) != 0):
        await delete_message(callback_query.from_user.id, callback_query)

    sql.change_msg(callback_query.from_user.id, msg.message_id)


    await callback_query.answer()

async def main() -> None:
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())