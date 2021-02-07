import random
import re

from pyrogram import filters
from pyrogram.errors import BadRequest

import alicia.helpers.fun_strings as fun
from alicia import LOGGER, OWNER_ID, alia, bot_id, bot_name
from alicia.helpers import extract_user
from alicia.utils import AioHttp, escape_markdown

MAX_MESSAGE_LENGTH = 4096


@alia.on_message(filters.command("runs"))
async def runs(client, message):
    await message.reply_text(random.choice(fun.RUN_STRINGS))


@alia.on_message(filters.command("slap"))
async def slap(client, message):
    text = message.text.split(None, 1)
    args = text[1]
    # reply to correct message
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    # get user who sent message
    if message.from_user.username:
        curr_user = "@" + escape_markdown(message.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            message.from_user.first_name, message.from_user.id
        )
    user_id = extract_user(message, args)
    if user_id:
        slapped_user = await client.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                slapped_user.first_name, slapped_user.id
            )
    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot_name, bot_id)
        user2 = curr_user
    temp = random.choice(fun.SLAP_TEMPLATES)
    item = random.choice(fun.ITEMS)
    hit = random.choice(fun.HIT)
    throw = random.choice(fun.THROW)
    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)
    reply_text(repl, parse_mode="markdown")


@alia.on_message(filters.command("punch"))
async def punch(client, message):
    text = message.text.split(None, 1)
    args = text[1]
    # reply to correct message
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    # get user who sent message
    if message.from_user.username:
        curr_user = "@" + escape_markdown(message.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            message.from_user.first_name, message.from_user.id
        )
    user_id = extract_user(message, args)
    if user_id:
        punched_user = await client.get_chat(user_id)
        user1 = curr_user
        if punched_user.username:
            user2 = "@" + escape_markdown(punched_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                punched_user.first_name, punched_user.id
            )
    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot_name, bot_id)
        user2 = curr_user
    temp = random.choice(fun.PUNCH_TEMPLATES)
    item = random.choice(fun.ITEMS)
    punch = random.choice(fun.PUNCH)
    repl = temp.format(user1=user1, user2=user2, item=item, punches=punch)
    reply_text(repl, parse_mode="markdown")


@alia.on_message(filters.command("hug"))
async def hug(client, message):
    text = message.split.text(None, 1)
    args = text[1]
    # reply to correct message
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    # get user who sent message
    if message.from_user.username:
        curr_user = "@" + escape_markdown(message.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(
            message.from_user.first_name, message.from_user.id
        )
    user_id = extract_user(message, args)
    if user_id:
        hugged_user = await client.get_chat(user_id)
        user1 = curr_user
        if hugged_user.username:
            user2 = "@" + escape_markdown(hugged_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(
                hugged_user.first_name, hugged_user.id
            )
    # if no target found, bot targets the sender
    else:
        user1 = "Awwh! [{}](tg://user?id={})".format(
            bot_name, bot_id
        )
        user2 = curr_user
    temp = random.choice(fun.HUG_TEMPLATES)
    hug = random.choice(fun.HUG)
    repl = temp.format(user1=user1, user2=user2, hug=hug)
    reply_text(repl, parse_mode="markdown")


@alia.on_message(filters.command("abuse"))
async def abuse(client, message):
    # reply to correct message
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    reply_text(random.choice(fun.ABUSE_STRINGS))


@alia.on_message(filters.command("dice"))
async def dice(client, message):
    await client.send_dice(message.chat.id)


@alia.on_message(filters.command("shrug"))
async def shrug(client, message):
    # reply to correct message
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    reply_text(random.choice(fun.SHGS))


@alia.on_message(filters.command("decide"))
async def yesnowtf(client, message):
    chat = message.chat
    res = await AioHttp().get_json("https://yesno.wtf/api")
    try:
        await client.send_animation(
            chat.id, animation=res["image"], caption=str(res["answer"]).upper()
        )
    except BadRequest:
        return


@alia.on_message(filters.command("table"))
async def table(client, message):
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    reply_text(random.choice(fun.TABLE))


@alia.on_message(filters.command("cri"))
async def cri(client, message):
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    reply_text(random.choice(fun.CRI))


@alia.on_message(filters.command("recite"))
async def recite(client, message):
    reply_text = (
        await message.reply_to_message.reply_text if message.reply_to_message else await message.reply_text
    )
    reply_text(random.choice(fun.BEING_LOGICAL))


@alia.on_message(filters.command("gbun"))
async def gbun(client, message):
    chat = message.chat
    if message.chat.type == "private":
        return
    await client.send_message(chat.id, (random.choice(fun.GBUN)))


@alia.on_message(filters.user(OWNER_ID) & filters.command("snipe"))
async def snipe(client, message):
    text = message.text.split(None, 1)
    args = text.split(None, 1)
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        await message.reply_text("Please give me a chat to echo to!")
    if len(args) >= 2:
        to_send = args[1]
        try:
            await client.send_message(int(chat_id), str(to_send))
        except Exception as excp:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            await message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group? Error {}".format(excp)
            )


@alia.on_message(filters.command("pasta"))
async def copypasta(client, message):
    if not message.reply_to_message:
        await message.reply_text("I need a message to make pasta.")
    else:
        emojis = [
            "😂",
            "😂",
            "👌",
            "✌",
            "💞",
            "👍",
            "👌",
            "💯",
            "🎶",
            "👀",
            "😂",
            "👓",
            "👏",
            "👐",
            "🍕",
            "💥",
            "🍴",
            "💦",
            "💦",
            "🍑",
            "🍆",
            "😩",
            "😏",
            "👉👌",
            "👀",
            "👅",
            "😩",
            "🚰",
        ]
        reply_text = random.choice(emojis)
        # choose a random character in the message to be substituted with 🅱️
        b_char = random.choice(message.reply_to_message.text).lower()
        for c in message.reply_to_message.text:
            if c == " ":
                reply_text += random.choice(emojis)
            elif c in emojis:
                reply_text += c
                reply_text += random.choice(emojis)
            elif c.lower() == b_char:
                reply_text += "🅱️"
            else:
                reply_text += c.upper() if bool(random.getrandbits(1)) else c.lower()
        reply_text += random.choice(emojis)
        await message.reply_to_message.reply_text(reply_text)


@alia.on_message(filters.command("clap"))
async def clapmoji(client, message):
    if not message.reply_to_message:
        await message.reply_text("I need a message to clap!")
    else:
        reply_text = "👏 "
        reply_text += message.reply_to_message.text.replace(" ", " 👏 ")
        reply_text += " 👏"
        await message.reply_to_message.reply_text(reply_text)


@alia.on_message(filters.command("owo"))
async def owo(client, message):
    if not message.reply_to_message:
        await message.reply_text("I need a message to meme.")
    else:
        faces = [
            "(・`ω´・)",
            ";;w;;",
            "owo",
            "UwU",
            ">w<",
            "^w^",
            r"\(^o\) (/o^)/",
            "( ^ _ ^)∠☆",
            "(ô_ô)",
            "~:o",
            ";____;",
            "(*^*)",
            "(>_",
            "(♥_♥)",
            "*(^O^)*",
            "((+_+))",
        ]
        reply_text = re.sub(r"[rl]", "w", message.reply_to_message.text)
        reply_text = re.sub(r"[ｒｌ]", "ｗ", message.reply_to_message.text)
        reply_text = re.sub(r"[RL]", "W", reply_text)
        reply_text = re.sub(r"[ＲＬ]", "Ｗ", reply_text)
        reply_text = re.sub(r"n([aeiouａｅｉｏｕ])", r"ny\1", reply_text)
        reply_text = re.sub(r"ｎ([ａｅｉｏｕ])", r"ｎｙ\1", reply_text)
        reply_text = re.sub(r"N([aeiouAEIOU])", r"Ny\1", reply_text)
        reply_text = re.sub(r"Ｎ([ａｅｉｏｕＡＥＩＯＵ])", r"Ｎｙ\1", reply_text)
        reply_text = re.sub(r"\!+", " " + random.choice(faces), reply_text)
        reply_text = re.sub(r"！+", " " + random.choice(faces), reply_text)
        reply_text = reply_text.replace("ove", "uv")
        reply_text = reply_text.replace("ｏｖｅ", "ｕｖ")
        reply_text += " " + random.choice(faces)
        await message.reply_to_message.reply_text(reply_text)


@alia.on_message(filters.command("iwi"))
async def iwi(client, message):
    if not message.reply_to_message:
        await message.reply_text("I niid missigi ti mimi.")
    else:
        reply_text = re.sub(r"(a|i|u|e|o)", "i", message.reply_to_message.text)
        reply_text = re.sub(r"(A|I|U|E|O)", "I", reply_text)
        await message.reply_to_message.reply_text(reply_text)


@alia.on_message(filters.command("mock"))
async def mock(client, message):
    if not message.reply_to_message:
        await message.reply_text("i nEeD MeSsAgE To mOcK.")
    else:
        reply_text = []
        for charac in message.reply_to_message.text:
            if charac.isalpha() and random.randint(0, 1):
                to_app = charac.upper() if charac.islower() else charac.lower()
                reply_text.append(to_app)
            else:
                reply_text.append(charac)
        await message.reply_to_message.reply_text("".join(reply_text))


@alia.on_message(filters.command("stretch"))
async def stretch(client, message):
    if not message.reply_to_message:
        message.reply_text("I need a message to streeeeeeeeetch.")
    else:
        count = random.randint(3, 10)
        reply_text = re.sub(
            r"([aeiouAEIOUａｅｉｏｕＡＥＩＯＵ])", (r"\1" * count), message.reply_to_message.text
        )
        if len(reply_text) >= MAX_MESSAGE_LENGTH:
            await message.reply_text(
                "Result of this message was too long for telegram!"
            )
            return
        await message.reply_to_message.reply_text(reply_text)


@alia.on_message(filters.regex(r"(?i)me too"))
async def me_too(client, message):
    reply = random.choice(["Me too thanks", "Haha yes, me too", "Same lol", "Me irl"])
    await message.reply_text(reply)


@alia.on_message(filters.regex(r"(?i)good night"))
async def goodnight(client, message):
    reply = random.choice(fun.GDNIGHT)
    await message.reply_text(reply, parse_mode="markdown")


@alia.on_message(filters.regex(r"(?i)good morning"))
async def goodmorning(client, message):
    reply = random.choice(fun.GDMORNING)
    message.reply_text(reply, parse_mode="markdown")


__help__ = """
Some dank memes for fun or whatever!

 × /shrug | /cri: Get shrug or ToT.
 × /decide: Randomly answer yes no etc.
 × /abuse: Abuses the retard!
 × /table: Flips a table...
 × /runs: Reply a random string from an array of replies.
 × /slap: Slap a user, or get slapped if not a reply.
 × /pasta: Famous copypasta meme, try and see.
 × /clap: Claps on someones message!
 × /owo: UwU-fy whole text XD.
 × /iwi: IwI-fy whili tixt XD
 × /roll: Rolls a dice.
 × /recite: Logical quotes to change your life.
 × /stretch:  streeeeeeetch iiiiiiit.
 × /warm: Hug a user warmly, or get hugged if not a reply.
 × /punch: Punch a user, or get punched if not a reply.
 × /mock: mOcKinG wHoLe TexT.

**Regex based memes:**

Some regex filters are:
`me too` | `good morning` | `good night`.

alicia will reply random strings accordingly when these words are used!
All regex filters can be disabled incase u don't want... like: `/disable metoo`.

"""

__mod_name__ = "Memes"
