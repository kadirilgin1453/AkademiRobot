# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Robot import SESSION_ADI, YETKILI

# Ana Butonlar
start_mesajı = "Hoş Geldin!\n/yardim alabilirsin"

start_butonu = [[InlineKeyboardButton("📚 Yardım", callback_data="yardim"), InlineKeyboardButton("ℹ️ Hakkımda", url="https://t.me/KekikAkademi")]]
start_butonu += [[InlineKeyboardButton("💸 Bağışta Bulun", url="https://t.me/KekikAkademi/1190")]]

yardim_butonu = [
    [
        InlineKeyboardButton("👤 Beni Gruba Ekle", url=f"https://t.me/{SESSION_ADI}?startgroup=ch"),
        InlineKeyboardButton("👷 Kodlarıma Ulaş", url="https://github.com/keyiflerolsun/AkademiRobot")
    ],
    [
        InlineKeyboardButton("🔙 Geri", callback_data="geri_don")
    ]
]

# Kullanıcı Kaydet
from Robot.Edevat.dict2json import dict2json
from Robot.Edevat._pyrogram.pyro_yardimcilari import kullanici

kullanicilar = f"{SESSION_ADI}_KULLANICILAR.json"

@Client.on_message(filters.command(['start'], ['!','.','/']))
async def start_buton(client:Client, message:Message):
    if message.chat.type == "private":
        #Kullanıcı Kaydet
        dict2json({
                'kullanici_id'  : message.from_user.id,
                'kullanici_nick': f"@{message.from_user.username}" if message.from_user.username else None,
                'kullanici_adi' : f"{message.from_user.first_name or ''} {message.from_user.last_name or ''}".strip()
            }, liste_key="kullanici_id", dosya_adi=kullanicilar)

        vatandas, _ = await kullanici(message)
        await client.send_document(YETKILI[0], kullanicilar, caption=f"{vatandas} __Eklendi..__")

    # Hoş Geldin Mesajı
    await message.reply(start_mesajı, reply_markup=InlineKeyboardMarkup(start_butonu))

@Client.on_callback_query(filters.regex(pattern=r"^geri_don$"))
async def geri_don_bilgisi(client:Client, callback_query:CallbackQuery):
    await callback_query.edit_message_text(start_mesajı, reply_markup=InlineKeyboardMarkup(start_butonu))
    await callback_query.answer('Afferin !\nGeri dönmeyi başaran ilk kişi oldun..', show_alert=True)

@Client.on_callback_query(filters.regex(pattern=r"^yardim$"))
async def yardim_bilgisi(client:Client, callback_query:CallbackQuery):
    await callback_query.edit_message_text(
        "__Ana Komutlarım Şunlar:__\n\n`.yardim`\n`.destek`\n`.logsalla`\n\n**Diğer komutlarım için /eklentilist'e bakabilirsin..**",
        reply_markup=InlineKeyboardMarkup(yardim_butonu)
    )

@Client.on_callback_query(filters.regex(pattern=r"^ana_sayfa$"))
async def ana_sayfa(client:Client, callback_query:CallbackQuery):
    await callback_query.edit_message_text(
        start_mesajı, reply_markup=InlineKeyboardMarkup(start_butonu)
    )
