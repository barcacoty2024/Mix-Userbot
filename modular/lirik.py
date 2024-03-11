import json
import urllib.parse
from urllib.request import Request, urlopen

from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "Lyric"
__help__ = "Lyrics"


async def search_lyrics(penyanyi, judul):
    try:
        penyanyi = urllib.parse.quote(penyanyi)
        judul = urllib.parse.quote(judul)

        url = f"https://api.lyrics.ovh/v1/{penyanyi}/{judul}"
        request = Request(url)

        with urlopen(request) as response:
            data = json.load(response)

            if "lyrics" in data:
                return data["lyrics"]
            else:
                return None
    except Exception as e:
        return None


@ky.ubot("lirik", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    try:
        pft = await m.reply(f"{em.proses} <b>Sedang mencari lirik lagu</b>")
        command = " ".join(m.command[1:])
        parts = command.split("-")
        if len(parts) != 2:
            await m.reply(
                f"{em.gagal} <b>Format perintah salah. Gunakan format: /lirik nama-penyanyi - judul-lagu</b>"
            )
            return

        penyanyi = parts[0].strip()
        judul = parts[1].strip()
        lyrics_text = await search_lyrics(penyanyi, judul)
        if not lyrics_text:
            lyrics_text = await search_lyrics(judul, penyanyi)

        if lyrics_text:
            await m.reply(f"{em.sukses} <code>{lyrics_text}</code>")
            await pft.delete()
        else:
            await m.reply(f"{em.gagal} <b>Maaf, lirik lagu tidak ditemukan.</b>")
            await pft.delete()
    except Exception as e:
        await m.reply(
            f"{em.gagal} <b>Terjadi kesalahan saat mencari lirik lagu.</b> <code>{e}</code>"
        )
        await pft.delete()
