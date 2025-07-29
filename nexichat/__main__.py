import sys
import asyncio
import importlib
import threading
from flask import Flask
from pyrogram import idle
from pyrogram.types import BotCommand

import config
from config import OWNER_ID
from nexichat import LOGGER, nexichat, load_clone_owners
from nexichat.modules import ALL_MODULES
from nexichat.modules.Clone import restart_bots


async def anony_boot():
    try:
        await nexichat.start()
        try:
            await nexichat.send_message(
                int(OWNER_ID),
                f"**{nexichat.me.mention} is started ✅**"
            )
        except Exception as ex:
            LOGGER.info(f"{nexichat.me.username} started, please start the bot from owner ID.")

        asyncio.create_task(restart_bots())
        await load_clone_owners()

    except Exception as ex:
        LOGGER.error(ex)

    for all_module in ALL_MODULES:
        try:
            importlib.import_module("nexichat.modules." + all_module)
            LOGGER.info(f"Successfully imported : {all_module}")
        except Exception as e:
            LOGGER.error(f"Failed to import module {all_module}: {e}")

    try:
        await nexichat.set_bot_commands(
            commands=[
                BotCommand("start", "Start the bot"),
                BotCommand("help", "Get the help menu"),
                BotCommand("clone", "Make your own chatbot"),
                BotCommand("cloned", "Get list of all cloned bots"),
                BotCommand("ping", "Check if the bot is alive"),
                BotCommand("id", "Get user ID"),
                BotCommand("stats", "Check bot stats"),
                BotCommand("gcast", "Broadcast message"),
                BotCommand("repo", "Get bot source code"),
            ]
        )
        LOGGER.info("Bot commands set successfully.")
    except Exception as ex:
        LOGGER.error(f"Failed to set bot commands: {ex}")

    LOGGER.info(f"@{nexichat.me.username} is running.")
    await idle()


# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_flask():
    app.run(host="0.0.0.0", port=8000)

# Start bot
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOGGER.info("Stopping nexichat Bot...")
