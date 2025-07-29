import logging
import time
import uvloop
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode
import config

# Performance
uvloop.install()

# Logging setup
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

# Globals
boot = time.time()
SUDOERS = set()
CLONE_OWNERS = {}

# Mongo
mongodb = MongoCli(config.MONGO_URL)
db = mongodb.Anonymous
cloneownerdb = db.clone_owners

def sudo():
    OWNER = config.OWNER_ID
    SUDOERS.add(OWNER)
    sudoersdb = db.sudoers
    async def _load():
        sudoers = await sudoersdb.find_one({"sudo": "sudo"})
        sudoers = sudoers.get("sudoers", []) if sudoers else []
        if OWNER not in sudoers:
            sudoers.append(OWNER)
            await sudoersdb.update_one({"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True)
        for x in sudoers:
            SUDOERS.add(x)
        print("Sudoers Loaded.")
    return _load

async def load_clone_owners():
    async for entry in cloneownerdb.find():
        CLONE_OWNERS[entry["bot_id"]] = entry["user_id"]

async def save_clonebot_owner(bot_id, user_id):
    await cloneownerdb.update_one({"bot_id": bot_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def get_clone_owner(bot_id):
    data = await cloneownerdb.find_one({"bot_id": bot_id})
    return data["user_id"] if data else None

async def delete_clone_owner(bot_id):
    await cloneownerdb.delete_one({"bot_id": bot_id})
    CLONE_OWNERS.pop(bot_id, None)

async def save_idclonebot_owner(clone_id, user_id):
    await cloneownerdb.update_one({"clone_id": clone_id}, {"$set": {"user_id": user_id}}, upsert=True)

async def get_idclone_owner(clone_id):
    data = await cloneownerdb.find_one({"clone_id": clone_id})
    return data["user_id"] if data else None

class NexiChat(Client):
    def __init__(self):
        super().__init__(
            name="nexichat",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

    async def stop(self):
        await super().stop()

# Create client instance
nexichat = NexiChat()
