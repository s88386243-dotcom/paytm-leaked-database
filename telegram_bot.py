import telebot
import requests
from telebot import types
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "📱 Welcome Sandesh Lookup Bot!\nSend me a mobile number to search.")

@bot.message_handler(func=lambda msg: True)
def lookup(message):
    mobile = message.text.strip()
    response = requests.get(API_URL + mobile)

    if response.status_code == 200:
        data = response.json()

        reply = (
            f"👤 Name: {data.get('name','-')}\n"
            f"📞 Mobile: {data.get('mobile','-')}\n"
            f"✉️ Email: {data.get('email','-')}\n"
            f"🏙️ City: {data.get('city','-')}\n"
            f"🕶️ Brand: {data.get('brand','-')}\n"
            f"👓 Item: {data.get('item_name','-')}\n"
            f"💰 Price: {data.get('item_price','-')}\n"
            f"🛒 Payment: {data.get('payment_method','-')}\n"
        )

        # 🔘 Buttons
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📂 View Full Record", callback_data=f"full_{mobile}")
        btn2 = types.InlineKeyboardButton("📝 Save to Logs", callback_data=f"log_{mobile}")
        markup.add(btn1, btn2)

        bot.send_message(message.chat.id, reply, reply_markup=markup)

    else:
        bot.reply_to(message, "❌ Record not found.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("full_"):
        mobile = call.data.split("_")[1]
        response = requests.get(API_URL + mobile)
        if response.status_code == 200:
            data = response.json()
            bot.send_message(call.message.chat.id, f"📂 Full Record:\n{data}")
    elif call.data.startswith("log_"):
        mobile = call.data.split("_")[1]
        bot.send_message(call.message.chat.id, f"✅ Search for {mobile} saved in logs!")

bot.polling()
