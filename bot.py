import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    PreCheckoutQuery,
    LabeledPrice,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

# 1. ВСТАВЬ СВОЙ ТОКЕН СЮДА
TOKEN = "8727002954:AAEArI2kY_icVEmFbCRyh46zDNl-e5jve9w"
PRICE_IN_STARS = 25  # <-- Цена в звёздах (можешь поменять на 1, 100 и т.д.)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- Приветствие и кнопка ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Создаем кнопку
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f"1. Donate {PRICE_IN_STARS} ⭐", 
                callback_data="donate"
            )]
        ]
    )
    # Отправляем приветствие на английском
    await message.answer(
        f"Hi, {message.from_user.first_name}! 👋\n\n"
        "Welcome to my bot.\n"
        f"Tap the button below to support the author with {PRICE_IN_STARS} Stars.",
        reply_markup=keyboard,
    )


# --- Обработка нажатия на кнопку ---
@dp.callback_query(F.data == "donate")
async def donate(callback: CallbackQuery):
    # Выставляем счет в Telegram Stars
    await callback.message.answer_invoice(
        title="Support the author ❤️",
        description=f"Thank you for your support! This is a donation of {PRICE_IN_STARS} Stars.",
        payload=f"donate_{PRICE_IN_STARS}",
        provider_token="",  # Для Stars ВСЕГДА должно быть пусто
        currency="XTR",     # XTR = Telegram Stars
        prices=[LabeledPrice(label="Donation", amount=PRICE_IN_STARS)],
    )
    await callback.answer()


# --- Подтверждение перед оплатой (обязательно) ---
@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)


# --- Сообщение после успешной оплаты ---
@dp.message(F.successful_payment)
async def payment_done(message: Message):
    await message.answer(
        f"🙏 Thank you! You successfully donated {message.successful_payment.total_amount} ⭐"
    )


# --- Запуск ---
async def main():
    print("Bot started on your PC...")
    await dp.start_polling(bot)


if __name__== "main":
    asyncio.run(main())