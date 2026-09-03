import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("👋 Hello", callback_data="hello"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [
            InlineKeyboardButton("📋 Help", callback_data="help"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "☺️Welcome to Aatroxa Bot!\n\n"
        "Choose an option below:",
        reply_markup=reply_markup,
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "hello":
        await query.edit_message_text(
            "👋 Hello! Nice to meet you!"
        )

    elif query.data == "about":
        await query.edit_message_text(
            "🤖 I'm Aatroxa Bot.\n"
            "Built for chaos, fun & vibes."
        )

    elif query.data == "help":
        await query.edit_message_text(
            "📋 Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show help"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Available commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )


def main():
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is not set!")

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
