from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import threading
import time

TOKEN = "8688610141:AAF6S7TKqidGrI4PjrcEhzh5PgGagb0b0J0"

running = False
success = 0
total = 0

MAX_RPS = 100
MAX_THREADS = 100

# lock для потоків, щоб не бились повідомлення
lock = threading.Lock()

def worker(url, rps, update: Update, context: ContextTypes.DEFAULT_TYPE):
    global success, total, running

    delay = 1 / rps

    while running:
        try:
            r = requests.get(url, timeout=3)
            code = r.status_code
            if code == 200:
                success += 1
        except:
            code = "ERR"

        total += 1

        # шлємо в чат кожен код, але через lock
        with lock:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Запит {total}: {code}")

        time.sleep(delay)

async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running, success, total

    if running:
        await update.message.reply_text("Вже працює 😏")
        return

    if len(context.args) != 3:
        await update.message.reply_text(
            "Формат:\n/start URL RPS THREADS\nПриклад:\n/start http://127.0.0.1:8000 5 5"
        )
        return

    url = context.args[0]

    try:
        rps = float(context.args[1])
        threads = int(context.args[2])
    except:
        await update.message.reply_text("Неправильні числа")
        return

    if rps > MAX_RPS or threads > MAX_THREADS:
        await update.message.reply_text("Занадто велике навантаження 🚫")
        return

    running = True
    success = 0
    total = 0

    for i in range(threads):
        t = threading.Thread(target=worker, args=(url, rps, update, context))
        t.daemon = True
        t.start()

    await update.message.reply_text(
        f"Запущено:\nURL: {url}\nRPS: {rps}\nThreads: {threads}"
    )

async def stop_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    running = False
    await update.message.reply_text("Зупинено 🛑")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Успішно: {success}\nВсього: {total}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_test))
app.add_handler(CommandHandler("stop", stop_test))
app.add_handler(CommandHandler("status", status))

app.run_polling()