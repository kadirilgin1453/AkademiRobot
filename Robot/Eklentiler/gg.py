# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from Robot import DESTEK_KOMUT
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "goygoy google linki verir..",
        "kullanim"  : [
            None
            ],
        "ornekler"  : [
            ".gg python nedir"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from Robot.Edevat._pyrogram.pyro_yardimcilari import yanitlanan_mesaj
from time import time
import requests

@Client.on_message(filters.command(['gg'], ['!','.','/']))
async def gg_komut(client:Client, message:Message):                           # fonksiyon oluşturuyoruz
    # < Başlangıç
    await log_yolla(client, message)
    yanit_id  = await yanitlanan_mesaj(message)
    ilk_mesaj = await message.reply("__Bekleyin..__",
        reply_to_message_id      = yanit_id,
        disable_web_page_preview = True
    )
    girilen_yazi        = message.command
    #------------------------------------------------------------- Başlangıç >

    if len(girilen_yazi) == 1:
        await ilk_mesaj.edit("**Arama yapabilmek için `bişeyler` girmelisiniz..**")
        return

    await ilk_mesaj.edit("`Aranıyor...`")

    basla = time()                                                          # Zamanı Başlat
    girdi = " ".join(girilen_yazi[1:])                                      # girdiyi komuttan ayrıştır

    mesaj = f"**Aranan :** `{girdi}`\n\n"                                   # Mesaj'ı Başlatıyoruz

    ara = girdi.replace(" ", "+")                                           # boşlukları + ya çeviriyoruz
    numune = f"https://da.gd/s?url=https://lmgtfy.com/?q={ara}%26iie=1"     # gg linkimize ekliyoruz
    api_tepki = requests.get(numune).text                                   # api tepkisini alıyoruz

    if api_tepki:                                                           # eğer tepki varsa
        mesaj += f"🔍 [{girdi}]({api_tepki.rstrip()})"                      # Mesaja Ekle
        bitir = time()                                                      # Zamanı Durdur
        sure = bitir - basla                                                # Duran - Başlayan Zaman
        mesaj += f"\n\n**Tepki Süresi :** `{str(sure)[:4]} sn`"             # Mesaja Ekle

        try:                                                                # Dene
            await ilk_mesaj.edit(mesaj, disable_web_page_preview = True)
        except Exception as hata:
            await hata_log(hata, client, ilk_mesaj)
            return
    else:                                                                   # Eğer tepki yoksa
        await ilk_mesaj.edit("__API Yanıt Vermedi Kanka..__")               # uyarı ver