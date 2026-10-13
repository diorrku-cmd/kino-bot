
import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

movies = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎬 Kino botga xush kelibsiz!\n\n"
        "/help — yordam\n"
        "/search — kino kodini yuborib qidiring"
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "🔎 Kino topish uchun kino kodini yozing.\n"
        "Admin kino qo‘shishi uchun /add buyrug‘idan foydalanadi."
    )

@bot.message_handler(commands=["add"])
def add_movie(message):
    bot.reply_to(
        message,
        "Admin funksiyasini keyingi bosqichda sozlaymiz."
    )

@bot.message_handler(func=lambda message: True)
def search_movie(message):
    code = message.text.strip()
    movie = movies.get(code)
    if movie:
        bot.reply_to(message, movie)
    else:
        bot.reply_to(
            message,
            "❌ Bu kod bo‘yicha kino topilmadi."
        )

bot.infinity_polling()
