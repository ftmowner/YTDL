from pyrogram import Client, filters
from database.db import db


@Client.on_message(filters.command("start"))
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    await message.reply_text("👋 Hello! Bot is running successfully!")
