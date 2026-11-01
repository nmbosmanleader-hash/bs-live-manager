
import os
import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@BS_COMMUNITY_01")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

START_TIME = time.time()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! BS Community Manager Bot is online.\n"
        "Commands: /live /stop /stats /id"
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Your Telegram ID: {update.effective_user.id}"
    )


def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID


async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="🔴 BS COMMUNITY LIVE is now active!\nJoin the live session."
    )
    await update.message.reply_text("Live announcement sent!")


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="⏹️ Live session announcement ended."
    )
    await update.message.reply_text("Live announcement ended!")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    uptime = int(time.time() - START_TIME)
    await update.message.reply_text(
        f"🤖 Bot is online\nUptime: {uptime} seconds"
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("live", live))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("stats", stats))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
