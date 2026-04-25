import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ТВОЇ ДАНІ
API_TOKEN = '7803945721:AAFHNSe-YtjaGCUUhfN7_vPe2jQpj0XI1Vg'
PRIVATE_CHANNEL_LINK = 'https://t.me/+Ay9Ar2AbZQ1mMDNl' # Посилання на твою приватку

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Кнопка оплати
def get_payment_keyboard():
    buttons = [[InlineKeyboardButton(text="💎 Купити Приват (25 ⭐)", callback_data="buy_stars")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в нашу приватку. Нажми кнопку, что бы получить доступ.", 
                         reply_markup=get_payment_keyboard())

@dp.callback_query(F.data == "buy_stars")
async def process_buy(callback: types.CallbackQuery):
    await bot.send_invoice(
        callback.from_user.id,
        title="Доступ до Приватки",
        description="Вход в закрытый канал навсегда!",
        payload="private_access_payload",
        provider_token="", # Для зірок залишаємо порожнім
        currency="XTR",   # Код для Telegram Stars
        prices=[LabeledPrice(label="⭐ Доступ", amount=25)]
    )

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer(f"✅ Оплата пройшла успешно! Твоя ссылка на вход:\n{PRIVATE_CHANNEL_LINK}")

if __name__ == "__main__":
    dp.run_polling(bot)