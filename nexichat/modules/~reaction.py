from pyrogram import Client, filters
from pyrogram.types import Message
from nexichat import nexichat

"""@nexichat.on_message(filters.incoming)
async def react_to_messages(client: Client, message: Message):
    try:
        await message.react("👍")
    except Exception as e:
        print(f"Failed to react to message: {e}")"""

from telethon import TelegramClient, events


@nexichat.on(events.NewMessage(incoming=True))
async def react_to_messages(event):
    try:
        await event.message.respond("👍")  # Telethon में `send_reaction` अभी Stable Version में नहीं है
    except Exception as e:
        print(f"Failed to react to message: {e}")

