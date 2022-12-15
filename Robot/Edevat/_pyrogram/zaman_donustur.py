# https://github.com/Skuzzy_xD/TelePyroBot

async def zaman_donustur(saniye: int) -> str:
    dakika, saniye  = divmod(saniye, 60)
    saat, dakika    = divmod(dakika, 60)
    gun, saat       = divmod(saat, 24)
    toparla = (
        (f"{str(gun)} gün, " if gun else "")
        + (f"{str(saat)} saat, " if saat else "")
        + (f"{str(dakika)} dakika, " if dakika else "")
        + (f"{str(saniye)} saniye, " if saniye else "")
    )
    return toparla[:-2]