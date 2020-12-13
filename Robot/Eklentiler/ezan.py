# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from Robot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama" : "KekikSpatula'dan ezan vakti bilgilerini verir..",
        "kullanim" : [
            "il"
            ],
        "ornekler" : [
            ".ezan çanakkale"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from Robot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from KekikSpatula import Ezan

@Client.on_message(filters.command(['ezan'],['!','.','/']))
async def ezan(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)
    yanit_id  = await yanitlanan_mesaj(message)
    ilk_mesaj = await message.reply("__Bekleyin..__",
        reply_to_message_id      = yanit_id,
        disable_web_page_preview = True
    )
    girilen_yazi = message.command
    #------------------------------------------------------------- Başlangıç >

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("__Arama yapabilmek için `il` girmelisiniz..__")
        return

    il   = girilen_yazi[1].replace('İ', "i").lower()  # komut hariç birinci kelime

    tr2eng  = str.maketrans(" .,-*/+-ıİüÜöÖçÇşŞğĞ", "________iIuUoOcCsSgG")
    il      = il.translate(tr2eng)

    try:
        ezan = Ezan(il).veri['veri'][0]
    except IndexError:
        await ilk_mesaj.edit(f'`{il}` __diye bir yer bulamadım..__')
        return

    mesaj = f"📍 `{ezan['il']}` __için Ezan Vakitleri;__\n\n"
    mesaj += f"🏙 **İmsak   :** `{ezan['imsak']}`\n"
    mesaj += f"🌅 **Güneş   :** `{ezan['gunes']}`\n"
    mesaj += f"🌇 **Öğle    :** `{ezan['ogle']}`\n"
    mesaj += f"🌆 **İkindi  :** `{ezan['ikindi']}`\n"
    mesaj += f"🌃 **Akşam   :** `{ezan['aksam']}`\n"
    mesaj += f"🌌 **Yatsı   :** `{ezan['yatsi']}`\n"

    try:
        await ilk_mesaj.edit(mesaj)
    except Exception as hata:
        await hata_log(hata, client, ilk_mesaj)
        return