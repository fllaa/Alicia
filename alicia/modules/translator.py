import os

from emoji import UNICODE_EMOJI
from google_trans_new import LANGUAGES, google_translator
from gtts import gTTS
from pyrogram import filters

from alicia import alia
from alicia.utils import AioHttp


@alia.on_message(filters.command("tr"))
async def gtrans(client, message):
    args = message.text.split(None, 1)
    if len(args) == 2:
        lang = args[1]
    else:
        lang = "en"
    try:
        translate_text = message.reply_to_message.text or message.reply_to_message.caption
    except AttributeError:
        await message.reply_text("What text I should translate?")
        return
    ignore_text = UNICODE_EMOJI.keys()
    for emoji in ignore_text:
        if emoji in translate_text:
            translate_text = translate_text.replace(emoji, "")

    translator = google_translator()
    try:
        translated = translator.translate(translate_text, lang_tgt=lang)
        source_lan = translator.detect(translate_text)[1].title()
        des_lan = LANGUAGES.get(lang).title()
        await message.reply_text(
            "Translated from {} to {}.\n {}".format(source_lan, des_lan, translated)
        )
    except BaseException as excp:
        await message.reply_text("Error: {}".format(excp))


@alia.on_message(filters.command("tts"))
async def gtts(client, message):
    args = message.text.split(None, 1)
    if len(args) == 2:
        reply = args[1]
    elif message.reply_to_message:
        reply = message.reply_to_message.text
    else:
        await message.reply_text(
            "Reply to some message or enter some text to convert it into audio format!"
        )
        return
    for x in "\n":
        reply = reply.replace(x, "")
    try:
        tts = gTTS(reply)
        tts.save("priscia.mp3")
        with open("priscia.mp3", "rb") as speech:
            await message.reply_audio(speech)
    finally:
        if os.path.isfile("priscia.mp3"):
            os.remove("priscia.mp3")


# Open API key
API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText"


@alia.on_message(filters.command("splcheck"))
async def spellcheck(client, message):
    if message.reply_to_message:
        text = message.reply_to_message.text

        params = dict(lang="US", clientVersion="2.0", apiKey=API_KEY, text=text)

        res = await AioHttp().get_json(URL, params)
        changes = res.get("LightGingerTheTextResult")
        curr_string = ""
        prev_end = 0

        for change in changes:
            start = change.get("From")
            end = change.get("To") + 1
            suggestions = change.get("Suggestions")
            if suggestions:
                # should look at this list more
                sugg_str = suggestions[0].get("Text")
                curr_string += text[prev_end:start] + sugg_str
                prev_end = end

        curr_string += text[prev_end:]
        await message.reply_text(curr_string)
    else:
        await message.reply_text(
            "Reply to some message to get grammar corrected text!"
        )


__help__ = """
× /tr or /tl: - To translate to your language, by default language is set to english, use `/tr <lang code>` for some other language!
× /splcheck: - As a reply to get grammar corrected text of gibberish message.
× /tts: - To some message to convert it into audio format!
"""
__mod_name__ = "Translate"
