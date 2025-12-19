from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from datetime import datetime, timedelta
import json, random, os

BOT_TOKEN = "8164828553:AAHleprVl8Xy0ln1d8Dbvbq0qGZm9X0QAj8"
ADMIN_ID = 7078812263   # yahan apna Telegram ID

DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        db = json.load(f)
else:
    db = {"users": {}, "last_period": 1000}

def save_db():
    with open(DATA_FILE, "w") as f:
        json.dump(db, f)

def is_paid(uid):
    if str(uid) in db["users"]:
        return datetime.fromisoformat(db["users"][str(uid)]) > datetime.now()
    return False

def next_period():
    db["last_period"] += 1
    save_db()
    return db["last_period"]

def prediction():
    return random.choice(["BIG", "SMALL"]), random.randint(60,75)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Daman Prediction Bot\n\n"
        "/predict - Prediction\n"
        "/status - Plan status\n"
        "/pay - Payment info\n"
        "/id - Your ID\n\n"
        "⚠️ Analysis only"
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not is_paid(uid):
        await update.message.reply_text("❌ Paid users only")
        return
    p, c = prediction()
    await update.message.reply_text(
        f"🎯 Prediction: {p}\n"
        f"📊 Confidence: {c}%\n"
        f"⏱ Period: {next_period()}\n"
        f"⚠️ Risk involved"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if is_paid(uid):
        await update.message.reply_text("✅ Plan Active")
    else:
        await update.message.reply_text("❌ No active plan")

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💳 VIP Plan\n₹299 / 30 Days\n\n"
        "UPI: yourupi@upi\n\n"
        "Payment ke baad /id + screenshot bheje"
    )

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your ID: {update.effective_user.id}")

async def addpaid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    uid = context.args[0]
    days = int(context.args[1])
    db["users"][uid] = (datetime.now()+timedelta(days=days)).isoformat()
    save_db()
    await update.message.reply_text("✅ User Activated")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("id", myid))
app.add_handler(CommandHandler("addpaid", addpaid))
app.run_polling()
