import os
import random
import logging
from telegram import InputMediaPhoto, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get token
telegram_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
if not telegram_bot_token:
    logging.error("Missing environment variable: TELEGRAM_BOT_TOKEN")
    exit()

# Start the bot
try:
    application = Application.builder().token(telegram_bot_token).build()
    logging.info("Telegram bot started successfully.")
except Exception as e:
    logging.error(f"Failed to create Telegram bot application: {e}")
    exit()


async def custom_dice(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE, 
    folder: str, 
    count: int, 
    faces: int = 6
):
    """
    dice rolling function to use custom dice images and make scaling easier.
    - folder: folder name where dice images are stored - and basically like the command name to make it easier to add new dice sets
    - count: number of dice to roll
    - faces: number of faces per dice (default 6)
    """
    results = [random.randint(1, faces) for _ in range(count)]
    logging.info(f"{update.effective_user} rolled {count}d{faces} in folder '{folder}': {results}")

    media_group = []
    for i, result in enumerate(results, 1):
        dice_file = f"./pic/{folder}/{i}_{result}.png"
        if os.path.exists(dice_file):
            media_group.append(InputMediaPhoto(open(dice_file, "rb")))
        else:
            logging.warning(f"Dice image not found: {dice_file}")

    if media_group:
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media_group)
    else:
        await update.message.reply_text(f"Results: {', '.join(map(str, results))}")


# roll 3 dices with 6 faces each with command /prost.
#also dont react to extra args, just ignore them and log that they were ignored.
async def prost(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        logging.info(f"Extra Args have been issued. Ignoring extra args for /prost: {context.args}")
    await custom_dice(update, context, folder="prost", count=3, faces=6)


# Add handler
application.add_handler(CommandHandler("prost", prost))

# Run the bot
application.run_polling(drop_pending_updates=True)
