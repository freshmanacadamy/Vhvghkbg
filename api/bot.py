from flask import Flask, request
import os
import telebot

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎉 *Bot is LIVE!*\n\nUse /help for commands", parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 
        "🤖 *Available Commands:*\n"
        "/start - Start bot\n"
        "/help - This message\n" 
        "/echo - Echo your text\n"
        "/info - Your info\n\n"
        "Built for Vercel 🚀",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['echo'])
def echo(message):
    bot.reply_to(message, "📝 Send me any text and I'll echo it back!")

@bot.message_handler(commands=['info'])
def info(message):
    user = message.from_user
    bot.reply_to(message, 
        f"👤 *Your Info:*\n"
        f"🆔 ID: `{user.id}`\n"
        f"📛 Name: {user.first_name}\n"
        f"🔗 Username: @{user.username or 'None'}\n"
        f"🌐 Language: {user.language_code or 'Unknown'}",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.startswith('/'):
        bot.reply_to(message, "❓ Unknown command. Use /help")
    else:
        bot.reply_to(message, f"🔁 Echo: {message.text}")

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        json_data = request.get_json()
        update = telebot.types.Update.de_json(json_data)
        bot.process_new_updates([update])
    return "✅ Telegram Bot Running on Vercel"

if __name__ == "__main__":
    app.run()
