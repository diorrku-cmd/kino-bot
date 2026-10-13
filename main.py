
import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

bot = telebot.TeleBot(TOKEN)
movies = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "🎬 KINO BOTGA XUSH KELIBSIZ!\n\n"
        "🔎 Kino kodini yuboring — kino qidiramiz.\n"
        "📌 Buyruqlar: /help"
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.reply_to(
        message,
        "🎥 Kino kodini yuboring.\n"
        "👑 Admin kino qo‘shishi: /add KOD\n"
        "Keyin kino video yoki faylini yuboring."
    )

@bot.message_handler(commands=["add"])
def add_movie(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⛔ Bu buyruq faqat admin uchun.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, "Misol: /add 101")
        return

    code = parts[1].strip()
    bot.reply_to(message, f"🎬 {code} kodi uchun kino videosini yuboring.")
    bot.register_next_step_handler(message, save_movie, code)

def save_movie(message, code):
    if message.content_type == "video":
        movies[code] = ("video", message.video.file_id)
    elif message.content_type == "document":
        movies[code] = ("document", message.document.file_id)
    else:
        bot.reply_to(message, "❌ Video yoki video fayl yuboring.")
        return

    bot.reply_to(message, f"✅ Kino saqlandi! Kodi: {code}")

@bot.message_handler(func=lambda message: True)
def search_movie(message):
    code = message.text.strip()
    movie = movies.get(code)

    if not movie:
        bot.reply_to(
            message,
            "❌ Kino topilmadi yoki bot qayta ishga tushgan.\n"
            "Admin kinoni qaytadan qo‘shishi kerak bo‘lishi mumkin."
        )
        return

    kind, file_id = movie
    if kind == "video":
        bot.send_video(message.chat.id, file_id)
    else:
        bot.send_document(message.chat.id, file_id)

bot.infinity_polling()
