import os
import json
import random
from datetime import time
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import( Application, CommandHandler, ContextTypes)

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TOKEN = "8851245383:AAH5etwRLacYrjXgvvLyTmBnSmBAdYWY8dg"

compliments = [
"Ти неймовірна, і кожен день поруч із тобою стає особливішим",
"Твоя посмішка здатна зробити навіть похмурий день прекрасним",
"У тебе неймовірна енергія, яку неможливо не помітити",
"Твої очі — це щось особливе, у них хочеться заглядати знову і знову",
"Ти заслуговуєш на все найкраще, що може подарувати цей світ",
"Ти справжня особливість, яку неможливо замінити",
"Ти виглядаєш прекрасно навіть тоді, коли думаєш, що це не так",
"Твій сміх — один із найприємніших звуків у світі",
"Поруч із тобою навіть звичайні моменти стають чарівними",
"Твоя ніжність — це справжній скарб",
"У тебе особливий погляд, який неможливо забути",
"Ти робиш цей світ красивішим",
"Ти як промінчик сонця в холодний день",
"Твоя присутність — це подарунок",
"Ти заслуговуєш чути компліменти щодня",
"Просто пам’ятай: ти чудова саме така, якою ти є",
"Ти — моя улюблена причина посміхатися",
"Кожен момент із тобою хочеться запам’ятати назавжди",
"Ти робиш моє життя теплішим",
"Ти — людина, про яку хочеться піклуватися",
"Ти особлива, і я дуже ціную тебе",
"Біля тебе серце почувається спокійніше",
"Ти — маленьке диво у великому світі",
"Доброго ранку, красуне. Нехай сьогоднішній день буде таким же прекрасним як твоя усмішка",
"Нехай сьогодні все виходить легко, бо ти цього варта",
"Твоя посмішка — найкращий початок будь-якого дня",
"Завтра буде новий день, і він стане кращим, бо в ньому є ти",
]

if os.path.exists("users.json"):
    with open("users.json", "r") as f:
        users = set(json.load(f))
else:
    users = set()

def save_users():
    with open("users.json", "w") as f:
        json.dump(list(users), f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_chat.id)
    save_users()

    await update.message.reply_text("Супер! Я буду надсилати тобі щоденні нагадування про те яка ти особлива")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id

    if user_id in users:
        users.remove(user_id)
        save_users()
        
        await update.message.reply_text ("Сумно :( Я більше не відправлятиму тобі компліменти")
    else:
        await update.message.reply_text("Тебе немає в списку ^_^")

def generate_compliment():
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Напиши один ніжний короткий комплімент українською мовою для дівчини. Додай красиві емодзі."
            }
        ]
    )
    return response.choices[0].message.content

async def send_compliment(context: ContextTypes.DEFAULT_TYPE):
    for user_id in users:
        if compliments:
            text = "Доброго ранку, сонечко☀️  n\n" + random.choice(compliments) + "\n\n🕊️🫂🩷"
        else:
            text = generate_compliment()

        await context.bot.send_message(
            chat_id=user_id,
            text=text
        )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))

app.job_queue.run_daily(
    send_compliment,
    time=time(hour=14, minute=23, tzinfo=ZoneInfo("Europe/London"))
)

import threading
from flask import Flask

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

def run_web():
    web_app.run(host="0.0.0.0", port=1000)

threading.Thread(target=run_web).start()

print ("Bot working!")

app.run_polling()
