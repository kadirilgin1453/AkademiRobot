# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from Robot.Edevat.zenginLog import log_yolla, hata_log
from Robot import DESTEK_KOMUT, SESSION_ADI
from pathlib import Path

DESTEK_KOMUT.update({
    Path(__file__).stem : {
        "aciklama"  : "nekobin.com ile entegreli paste hizmeti..\nkodu paste yapar, paste linkini betiğe çevirir..",
        "kullanim"  : [
            "Yanıtlanan Mesaj",
            "Yanıtlanan Dosya",
            "Metin"
            ],
        "ornekler"  : [
            ".nekover py «__yanıtlanan kod__»",
            ".nekover go «__yanıtlanan dosya__»",
            ".nekoal «__yanıtlanan nekobin linki__»"
            ]
    }
})

from pyrogram import Client, filters
from pyrogram.types import Message
from Robot.Edevat.link_ayikla import link_ayikla
import aiohttp, os, requests

@Client.on_message(filters.command(['nekover'], ['!','.','/']))
async def nekover(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)

    ilk_mesaj = await message.reply("⌛️ `Hallediyorum..`",
        quote                    = True,
        disable_web_page_preview = True
    )
    girilen_yazi        = message.command
    cevaplanan_mesaj    = message.reply_to_message
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` ve `kod` vermelisiniz..__")
            return
        elif len(girilen_yazi) == 2:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` **da** vermelisiniz..__\n\n`.nekover py` **kod**")
            return

        kod = " ".join(girilen_yazi[2:]) 

    elif cevaplanan_mesaj and cevaplanan_mesaj.document:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` **da** vermelisiniz..__\n\n`.nekover py`")
            return

        gelen_dosya = await cevaplanan_mesaj.download()

        veri_listesi = None
        with open(gelen_dosya, "rb") as oku:
            veri_listesi = oku.readlines()

        kod = "".join(veri.decode("UTF-8") for veri in veri_listesi)

        os.remove(gelen_dosya)

    elif cevaplanan_mesaj.text:
        if len(girilen_yazi) == 1:
            await ilk_mesaj.edit("__Paste yapabilmek için `uzantı` **da** vermelisiniz..__\n\n`.nekover py`")
            return
        kod = cevaplanan_mesaj.text

    else:
        await ilk_mesaj.edit("__güldük__")
        return

    uzanti = message.command[1]
    await ilk_mesaj.delete()

    async with aiohttp.ClientSession() as session:
        async with session.post(
                'https://nekobin.com/api/documents',
                json={"content": kod},
                timeout=3
        ) as response:
            key = (await response.json())["result"]["key"]

    await message.reply(f'__@{SESSION_ADI} tarafından dönüştürülmüştür..__\n\n**https://nekobin.com/{key}.{uzanti}**',
                  disable_web_page_preview  = True,
                  reply_to_message_id       = yanit_id
    )

@Client.on_message(filters.command(['nekoal'], ['!','.','/']))
async def nekoal(client:Client, message:Message):
    # < Başlangıç
    await log_yolla(client, message)

    ilk_mesaj = await message.reply("⌛️ `Hallediyorum..`",
        quote                    = True,
        disable_web_page_preview = True
    )
    cevaplanan_mesaj    = message.reply_to_message
    ayiklanan_linkler   = await link_ayikla(cevaplanan_mesaj.text)
    #------------------------------------------------------------- Başlangıç >

    if cevaplanan_mesaj is None:
        await ilk_mesaj.edit("__script'e çevrilecek nekobin linki yanıtlamanız gerekli..__")
        return
    elif not ayiklanan_linkler[0].startswith("https://nekobin.com"):
        await ilk_mesaj.edit("__sadece nekobin linki yanıtlaman gerekli..__\n\n`.nekoal`")
        return

    kod = cevaplanan_mesaj.text.split('/')[-1]
    raw = 'https://nekobin.com/raw/' + kod

    try:
        data = requests.get(raw).content
    except Exception as hata:
        await hata_log(hata, client, ilk_mesaj)
        return

    await ilk_mesaj.delete()

    with open(f'{kod}', "wb+") as dosya: dosya.write(data)

    await message.reply_document(
            document                    = f"{kod}",
            caption                     = f'__@{SESSION_ADI} tarafından dönüştürülmüştür..__',
            disable_notification        = True,
            reply_to_message_id         = cevaplanan_mesaj.message_id
    )
    os.remove(f"{kod}")