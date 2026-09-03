import os
import random
import time

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


# ============================================================
# GAME DATA
# ============================================================

coins = {}
daily_claims = {}

grid_games = {}

word_chain_games = {}
word_chain_used = {}


# ============================================================
# START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("👋 Hello", callback_data="hello"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
        [
            InlineKeyboardButton("🎮 Games", callback_data="games"),
            InlineKeyboardButton("💰 Economy", callback_data="economy"),
        ],
        [
            InlineKeyboardButton("📋 Help", callback_data="help"),
        ],
    ]

    await update.message.reply_text(
        "🚀 Welcome to Aatroxa Bot!\n\n"
        "🎮 Games\n"
        "💰 Rewards\n"
        "🏆 Challenges\n\n"
        "Choose an option below:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    # --------------------------------------------------------
    # HELLO
    # --------------------------------------------------------

    if query.data == "hello":

        await query.edit_message_text(
            "👋 Hello!\n\n"
            "Welcome to Aatroxa Bot 😎"
        )

    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    elif query.data == "about":

        await query.edit_message_text(
            "🤖 Aatroxa Bot\n\n"
            "🎮 Games\n"
            "💰 Economy\n"
            "🎁 Daily rewards\n"
            "🔤 Word chain\n"
            "🟩 Grid treasure\n\n"
            "Have fun! 🔥"
        )

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    elif query.data == "help":

        await query.edit_message_text(
            "📋 AATROXA COMMANDS\n\n"

            "🤖 GENERAL\n"
            "/start - Start the bot\n"
            "/help - Show this menu\n\n"

            "💰 ECONOMY\n"
            "/daily - Daily reward\n"
            "/balance - Check coins\n\n"

            "🎮 GAMES\n"
            "/games - Game menu\n"
            "/dice - Roll dice\n"
            "/coinflip - Flip coin\n"
            "/rps - Rock Paper Scissors\n"
            "/guess 5 - Guess number\n"
            "/grid - Treasure grid\n"
            "/wordchain - Start word chain\n"
            "/word elephant - Continue chain"
        )

    # --------------------------------------------------------
    # GAMES MENU
    # --------------------------------------------------------

    elif query.data == "games":

        keyboard = [
            [
                InlineKeyboardButton("🎲 Dice", callback_data="dice"),
                InlineKeyboardButton("🪙 Coin", callback_data="coin"),
            ],
            [
                InlineKeyboardButton("✊ RPS", callback_data="rps"),
                InlineKeyboardButton("🔢 Guess", callback_data="guess"),
            ],
            [
                InlineKeyboardButton("🟩 Grid", callback_data="grid"),
                InlineKeyboardButton("🔤 Word Chain", callback_data="wordchain"),
            ],
        ]

        await query.edit_message_text(
            "🎮 GAME CENTER\n\n"
            "Choose a game:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # --------------------------------------------------------
    # ECONOMY MENU
    # --------------------------------------------------------

    elif query.data == "economy":

        balance_amount = coins.get(user_id, 0)

        keyboard = [
            [
                InlineKeyboardButton("🎁 Daily Reward", callback_data="daily"),
            ],
            [
                InlineKeyboardButton("💰 Balance", callback_data="balance"),
            ],
        ]

        await query.edit_message_text(
            f"💰 ECONOMY\n\n"
            f"Your balance: {balance_amount} coins\n\n"
            f"Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # --------------------------------------------------------
    # DICE
    # --------------------------------------------------------

    elif query.data == "dice":

        number = random.randint(1, 6)

        await query.edit_message_text(
            f"🎲 You rolled a **{number}**!",
            parse_mode="Markdown",
        )

    # --------------------------------------------------------
    # COIN
    # --------------------------------------------------------

    elif query.data == "coin":

        result = random.choice(["Heads 🪙", "Tails 🪙"])

        await query.edit_message_text(
            f"🪙 The coin landed on **{result}**!",
            parse_mode="Markdown",
        )

    # --------------------------------------------------------
    # RPS MENU
    # --------------------------------------------------------

    elif query.data == "rps":

        keyboard = [
            [
                InlineKeyboardButton("✊ Rock", callback_data="rock"),
                InlineKeyboardButton("📄 Paper", callback_data="paper"),
                InlineKeyboardButton("✂️ Scissors", callback_data="scissors"),
            ]
        ]

        await query.edit_message_text(
            "✊📄✂️ ROCK PAPER SCISSORS\n\n"
            "Choose your move:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # --------------------------------------------------------
    # RPS GAME
    # --------------------------------------------------------

    elif query.data in ["rock", "paper", "scissors"]:

        choices = ["rock", "paper", "scissors"]

        bot_choice = random.choice(choices)

        emojis = {
            "rock": "✊",
            "paper": "📄",
            "scissors": "✂️",
        }

        player = query.data

        if player == bot_choice:

            result = "🤝 It's a draw!"

        elif (
            (player == "rock" and bot_choice == "scissors")
            or
            (player == "paper" and bot_choice == "rock")
            or
            (player == "scissors" and bot_choice == "paper")
        ):

            result = "🎉 You win!"

        else:

            result = "😂 I win!"

        await query.edit_message_text(
            f"You: {emojis[player]}\n"
            f"Bot: {emojis[bot_choice]}\n\n"
            f"{result}"
        )

    # --------------------------------------------------------
    # GUESS
    # --------------------------------------------------------

    elif query.data == "guess":

        await query.edit_message_text(
            "🔢 GUESSING GAME\n\n"
            "I'm thinking of a number from 1 to 10.\n\n"
            "Use:\n"
            "/guess 5\n\n"
            "Good luck! 🍀"
        )

    # --------------------------------------------------------
    # GRID
    # --------------------------------------------------------

    elif query.data == "grid":

        await send_grid(query, user_id)

    # --------------------------------------------------------
    # GRID SQUARE
    # --------------------------------------------------------

    elif query.data.startswith("grid_"):

        position = int(query.data.split("_")[1])

        treasure = grid_games.get(user_id)

        if treasure is None:

            await query.edit_message_text(
                "❌ This game has expired.\n\n"
                "Use /grid to start a new game."
            )

            return

        if position == treasure:

            reward = random.randint(50, 200)

            coins[user_id] = coins.get(user_id, 0) + reward

            del grid_games[user_id]

            await query.edit_message_text(
                f"💎 TREASURE FOUND! 🎉\n\n"
                f"💰 You won {reward} coins!\n"
                f"💵 Balance: {coins[user_id]} coins"
            )

        else:

            del grid_games[user_id]

            await query.edit_message_text(
                "💨 Empty square!\n\n"
                "The treasure escaped! 😭\n\n"
                "Use /grid to try again."
            )

    # --------------------------------------------------------
    # WORD CHAIN
    # --------------------------------------------------------

    elif query.data == "wordchain":

        await query.edit_message_text(
            "🔤 WORD CHAIN\n\n"
            "Start the game with:\n\n"
            "/wordchain\n\n"
            "Then continue with:\n\n"
            "/word elephant"
        )


# ============================================================
# HELP
# ============================================================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📋 AATROXA BOT\n\n"

        "🤖 GENERAL\n"
        "/start\n"
        "/help\n\n"

        "💰 ECONOMY\n"
        "/daily\n"
        "/balance\n\n"

        "🎮 GAMES\n"
        "/games\n"
        "/dice\n"
        "/coinflip\n"
        "/rps\n"
        "/guess 5\n"
        "/grid\n"
        "/wordchain\n"
        "/word elephant"
    )


# ============================================================
# GAMES MENU
# ============================================================

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🎲 Dice", callback_data="dice"),
            InlineKeyboardButton("🪙 Coin", callback_data="coin"),
        ],
        [
            InlineKeyboardButton("✊ RPS", callback_data="rps"),
            InlineKeyboardButton("🔢 Guess", callback_data="guess"),
        ],
        [
            InlineKeyboardButton("🟩 Grid", callback_data="grid"),
            InlineKeyboardButton("🔤 Word Chain", callback_data="wordchain"),
        ],
    ]

    await update.message.reply_text(
        "🎮 GAME CENTER\n\n"
        "Choose a game:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# DICE
# ============================================================

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    number = random.randint(1, 6)

    await update.message.reply_text(
        f"🎲 You rolled: **{number}**",
        parse_mode="Markdown",
    )


# ============================================================
# COIN FLIP
# ============================================================

async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):

    result = random.choice([
        "Heads 🪙",
        "Tails 🪙"
    ])

    await update.message.reply_text(
        f"🪙 **{result}**!",
        parse_mode="Markdown",
    )


# ============================================================
# RPS
# ============================================================

async def rps(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("✊ Rock", callback_data="rock"),
            InlineKeyboardButton("📄 Paper", callback_data="paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="scissors"),
        ]
    ]

    await update.message.reply_text(
        "✊📄✂️ Choose your move:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# GUESSING GAME
# ============================================================

async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:

        await update.message.reply_text(
            "🔢 Pick a number from 1 to 10.\n\n"
            "Example:\n"
            "/guess 7"
        )

        return

    try:

        player_number = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "❌ Please enter a number."
        )

        return

    if player_number < 1 or player_number > 10:

        await update.message.reply_text(
            "⚠️ Choose a number from 1 to 10."
        )

        return

    bot_number = random.randint(1, 10)

    if player_number == bot_number:

        reward = random.randint(20, 50)

        user_id = update.effective_user.id

        coins[user_id] = coins.get(user_id, 0) + reward

        await update.message.reply_text(
            f"🎉 JACKPOT!\n\n"
            f"The number was {bot_number}!\n"
            f"💰 You won {reward} coins!"
        )

    else:

        await update.message.reply_text(
            f"❌ Nope!\n\n"
            f"You guessed: {player_number}\n"
            f"My number was: {bot_number}"
        )


# ============================================================
# DAILY REWARD
# ============================================================

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    now = time.time()

    last_claim = daily_claims.get(user_id, 0)

    if now - last_claim < 86400:

        remaining = int(
            86400 - (now - last_claim)
        )

        hours = remaining // 3600

        minutes = (remaining % 3600) // 60

        await update.message.reply_text(
            f"⏳ You already claimed your reward!\n\n"
            f"Come back in {hours}h {minutes}m."
        )

        return

    reward = random.randint(50, 150)

    coins[user_id] = coins.get(user_id, 0) + reward

    daily_claims[user_id] = now

    await update.message.reply_text(
        f"🎁 DAILY REWARD!\n\n"
        f"💰 You received {reward} coins!\n"
        f"💵 Balance: {coins[user_id]} coins\n\n"
        f"Come back tomorrow! 🔥"
    )


# ============================================================
# BALANCE
# ============================================================

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    amount = coins.get(user_id, 0)

    await update.message.reply_text(
        f"💰 Your balance: {amount} coins"
    )


# ============================================================
# GRID GAME
# ============================================================

async def grid(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    await create_grid(update, user_id)


async def create_grid(update, user_id):

    treasure = random.randint(0, 8)

    grid_games[user_id] = treasure

    keyboard = []

    for row in range(3):

        buttons = []

        for col in range(3):

            position = row * 3 + col

            buttons.append(
                InlineKeyboardButton(
                    "⬜",
                    callback_data=f"grid_{position}"
                )
            )

        keyboard.append(buttons)

    await update.message.reply_text(
        "🟩 MYSTERY GRID\n\n"
        "💎 One square contains treasure!\n\n"
        "Choose a square:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def send_grid(query, user_id):

    treasure = random.randint(0, 8)

    grid_games[user_id] = treasure

    keyboard = []

    for row in range(3):

        buttons = []

        for col in range(3):

            position = row * 3 + col

            buttons.append(
                InlineKeyboardButton(
                    "⬜",
                    callback_data=f"grid_{position}"
                )
            )

        keyboard.append(buttons)

    await query.edit_message_text(
        "🟩 MYSTERY GRID\n\n"
        "💎 Find the hidden treasure!\n\n"
        "Choose a square:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ============================================================
# WORD CHAIN
# ============================================================

async def wordchain(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    word_chain_games[chat_id] = "apple"

    word_chain_used[chat_id] = {"apple"}

    await update.message.reply_text(
        "🔤 WORD CHAIN STARTED!\n\n"
        "Starting word: 🍎 apple\n\n"
        "Your word must start with:\n"
        "👉 E\n\n"
        "Example:\n"
        "/word elephant"
    )


async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id not in word_chain_games:

        await update.message.reply_text(
            "❌ No word-chain game is running.\n\n"
            "Use /wordchain first!"
        )

        return

    if not context.args:

        await update.message.reply_text(
            "🔤 Enter a word.\n\n"
            "Example:\n"
            "/word elephant"
        )

        return

    new_word = context.args[0].lower().strip()

    last_word = word_chain_games[chat_id]

    required_letter = last_word[-1]

    if not new_word.isalpha():

        await update.message.reply_text(
            "❌ Please enter a normal word."
        )

        return

    if new_word in word_chain_used[chat_id]:

        await update.message.reply_text(
            "❌ That word was already used!"
        )

        return

    if new_word[0] != required_letter:

        await update.message.reply_text(
            f"❌ Wrong letter!\n\n"
            f"Your word must start with "
            f"{required_letter.upper()}."
        )

        return

    word_chain_games[chat_id] = new_word

    word_chain_used[chat_id].add(new_word)

    reward = random.randint(5, 20)

    user_id = update.effective_user.id

    coins[user_id] = coins.get(user_id, 0) + reward

    await update.message.reply_text(
        f"✅ {new_word}\n\n"
        f"🔥 Good chain!\n\n"
        f"Next letter: "
        f"{new_word[-1].upper()}\n\n"
        f"💰 +{reward} coins"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:

        raise ValueError(
            "BOT_TOKEN is not set!"
        )

    app = Application.builder().token(token).build()

    # Commands

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("games", games)
    )

    app.add_handler(
        CommandHandler("dice", dice)
    )

    app.add_handler(
        CommandHandler("coinflip", coinflip)
    )

    app.add_handler(
        CommandHandler("rps", rps)
    )

    app.add_handler(
        CommandHandler("guess", guess)
    )

    app.add_handler(
        CommandHandler("daily", daily)
    )

    app.add_handler(
        CommandHandler("balance", balance)
    )

    app.add_handler(
        CommandHandler("grid", grid)
    )

    app.add_handler(
        CommandHandler("wordchain", wordchain)
    )

    app.add_handler(
        CommandHandler("word", word)
    )

    # Buttons

    app.add_handler(
        CallbackQueryHandler(button)
    )

    print("🤖 Aatroxa Bot is running...")

    app.run_polling()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
