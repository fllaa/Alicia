from pyrogram import filters

from alicia import alia, BRAINLY_API
from alicia.utils import AioHttp

@alia.on_message(filters.command("brainly"))
async def brainly(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.reply_text("Nanya apaan sih lu gajelas")
        return
    splt = args[1].split()
    tanya = "%20".join(splt)
    url = "https://rest.farzain.com/api/brainly.php?id={}&apikey={}".format(tanya, BRAINLY_API)
    json = await AioHttp().get_json(url)
    result = "Hasil pencarian untuk <b>{}</b> di Brainly".format(args[1])
    for x in json:
        title = x["title"]
        link = x["url"]
        result += f"× <a href='{link}'>{title}</a>\n"
    await message.reply_text(
        result,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

__help__ = """
Cari semua pertanyaanmu di Brainly

**Available commands:**

× `/brainly <query>`: tanya pertanyaan di brainly.co.id

"""

__mod_name__ = "Brainly"
