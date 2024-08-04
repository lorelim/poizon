import aiogram
from aiogram import types

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

button1_main = InlineKeyboardButton(text = "Калькулятор стоимости", callback_data = "main1")
button2_main = InlineKeyboardButton(text = "Отзывы о нашей работе", callback_data = "main2", url = "https://t.me/poshoozim_feedback")
button3_main = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main3", url = "https://t.me/POSHOOZIM_MANAGER")

#create main keyboard
kb_main = InlineKeyboardMarkup( inline_keyboard = [[button1_main], [button2_main], [button3_main]])

button1_calc = InlineKeyboardButton(text = "Кросовки/Ботинки", callback_data = "calc1")
button2_calc = InlineKeyboardButton(text = "Кофты/Штаны/Брюки/Джинсы", callback_data = "calc2")
button3_calc = InlineKeyboardButton(text = "Майки/Рубашки/Шорты", callback_data = "calc3")
button4_calc = InlineKeyboardButton(text = "Куртки", callback_data = "calc4")
button5_calc = InlineKeyboardButton(text = "Аксессуары/Парфюм", callback_data = "calc5")
button6_calc = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main3", url = "https://t.me/POSHOOZIM_MANAGER")
button7_calc = InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu")

#create a keybord for order 
kb_calc = InlineKeyboardMarkup(inline_keyboard = [[button1_calc], [button2_calc], [button3_calc], [button4_calc], [button5_calc],[button6_calc], [button7_calc]])


button1_order_product = InlineKeyboardButton(text = "Вернуться в меню", callback_data = "menu")
button2_order_product = InlineKeyboardButton(text = "Связаться с нами", callback_data = "main4", url = "https://t.me/POSHOOZIM_MANAGER")
kb_order_product = InlineKeyboardMarkup(inline_keyboard = [[button2_order_product], [button1_order_product]])

