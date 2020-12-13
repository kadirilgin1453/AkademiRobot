# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters
from pyrogram.types import Message
from Robot import YETKILI

@Client.on_message(filters.sticker)
async def disc(client:Client, message:Message):
    if (message.sticker) and (str(message.from_user.id) not in YETKILI):
        await message.delete()