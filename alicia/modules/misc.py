import asyncio
import html
import random
import re
from random import randint

import wikipedia
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw.types import MessageEntityMentionName

from alicia import (
    OWNER_ID,
    WALL_API,
    alia,
    bot_id,
    spamwtc,
)
from alicia.__main__ import GDPR, STATS, USER_INFO
from alicia.helpers import extract_user
from alicia.utils import AioHttp, escape_markdown, mention_html


@alia.on_message(filters.command("id"))
async def get_id(client, message):
    args = message.text.split(None, 1)[1]
    user_id = extract_user(message, args)
    if user_id:
        if (
            message.reply_to_message
            and message.reply_to_message.forward_from
        ):
            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from
            await message.reply_text(
                "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.".format(
                    escape_markdown(user2.first_name),
                    user2.id,
                    escape_markdown(user1.first_name),
                    user1.id,
                ),
                parse_mode="markdown",
            )
        else:
            user = await client.get_chat(user_id)
            await message.reply_text(
                "{}'s id is `{}`.".format(escape_markdown(user.first_name), user.id),
                parse_mode="markdown",
            )
    else:
        if message.chat.type == "private":
            await message.reply_text(
                "Your id is `{}`.".format(message.from_user.id), parse_mode="markdown"
            )

        else:
            await message.reply_text(
                "This group's id is `{}`.".format(message.chat.id),
                parse_mode="markdown",
            )


@alia.on_message(filters.command("info"))
async def info(client, message):
    args = message.text.split(None, 1)[1]
    user_id = extract_user(message, args)
    chat = message.chat
    if user_id:
        user = await client.get_chat(user_id)
    elif not message.reply_to_message and not args:
        user = message.from_user
    elif not message.reply_to_message and (
        not args
        or (
            len(args) >= 1
            and not args[0].startswith("@")
            and not args[0].isdigit()
            and not message.entities == MessageEntityMentionName
        )
    ):
        await message.reply_text("I can't extract a user from this.")
        return
    else:
        return
    del_msg = await message.reply_text(
        "Hold tight while I steal some data from <b>FBI Database</b>...",
        parse_mode="HTML",
    )
    text = (
        "<b>USER INFO</b>:"
        "\n\nID: <code>{}</code>"
        "\nFirst Name: {}".format(user.id, html.escape(user.first_name))
    )
    if user.last_name:
        text += "\nLast Name: {}".format(html.escape(user.last_name))
    if user.username:
        text += "\nUsername: @{}".format(html.escape(user.username))
    text += "\nPermanent user link: {}".format(mention_html(user.id, "link"))
    text += "\nNumber of profile pics: {}".format(
        await client.get_profile_photos_count(user.id)
    )
    try:
        sw = spamwtc.get_ban(int(user.id))
        if sw:
            text += "\n\n<b>This person is banned in Spamwatch!</b>"
            text += f"\nResason: <pre>{sw.reason}</pre>"
    except BaseException:
        pass  # Don't break on exceptions like if api is down?

    if user.id == OWNER_ID:
        text += "\n\nAye this guy is my owner.\nI would never do anything against him!"
    elif user.id == int(1087968824):
        text += "\n\nThis person is anonymous admin in this group. "
    try:
        memstatus = chat.get_member(user.id).status
        if memstatus in ["administrator", "creator"]:
            result = await client.get_chat_member(chat.id, user.id)
            if result.title:
                text += f"\n\nThis user has custom title <b>{result.title}</b> in this chat."
    except BadRequest:
        pass
    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info
    try:
        profile = await client.get_user_profile_photos(user.id).file_id
        await client.send_chat_action(chat.id, "upload_photo")
        await client.send_photo(
            chat.id,
            photo=profile,
            caption=(text),
            parse_mode="HTML",
        )
    except IndexError:
        await client.send_chat_action(chat.id, "typing")
        await message.reply_text(text, parse_mode="HTML", disable_web_page_preview=True)
    finally:
        del_msg.delete()


@alia.on_message(filters.user(OWNER_ID) & filters.command("echo"))
async def echo(client, message):
    args = message.text.split(None, 1)
    if message.reply_to_message:
        await message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)
    message.delete()


@alia.on_message(filters.user(OWNER_ID) & filters.command("gdpr"))
async def gdpr(client, message):
    await message.reply_text("Deleting identifiable data...")
    for mod in GDPR:
        mod.__gdpr__(message.from_user.id)
    await message.reply_text(
        "Your personal data has been deleted.\n\nNote that this will not unban "
        "you from any chats, as that is telegram data, not Alicia data. "
        "Flooding, warns, and gbans are also preserved, as of "
        "[this](https://ico.org.uk/for-organisations/guide-to-the-general-data-protection-regulation-gdpr/individual-rights/right-to-erasure/), "
        "which clearly states that the right to erasure does not apply "
        '"for the performance of a task carried out in the public interest", as is '
        "the case for the aforementioned pieces of data.",
        parse_mode="markdown",
    )


MARKDOWN_HELP = """
Markdown is a very powerful formatting tool supported by telegram. Alicia has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

- <code>_italic_</code>: wrapping text with '_' will produce italic text
- <code>*bold*</code>: wrapping text with '*' will produce bold text
- <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
- <code>~strike~</code> wrapping text with '~' will produce strikethrough text
- <code>--underline--</code> wrapping text with '--' will produce underline text
- <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
EG: <code>[test](example.com)</code>

- <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
EG: <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
"""

@alia.on_message(filters.private & filters.command("markdownhelp"))
async def markdown_help(client, message):
    asyncio.gather(
        message.reply_text(MARKDOWN_HELP, parse_mode="HTML"),
        message.reply_text(
            "Try forwarding the following message to me, and you'll see!"
        ),
        message.reply_text(
            "/save test This is a markdown test. _italics_, --underline--, *bold*, `code`, ~strike~ "
            "[URL](example.com) [button](buttonurl:github.com) "
            "[button2](buttonurl://google.com:same)"
        ),
    )


@alia.on_message(filters.command("wiki"))
async def wiki(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.reply_text("Enter keywords")
        return
    kueri = re.split(pattern="wiki", string=args[1])
    wikipedia.set_lang("en")
    try:
        pertama = await message.reply_text("🔄 Loading...")
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="🔧 More Info...", url=wikipedia.page(kueri).url
                    )
                ]
            ]
        )
        await pertama.edit_text(
                text=wikipedia.summary(kueri, sentences=10),
                reply_markup=keyboard,
        )
    except wikipedia.PageError as e:
        await message.reply_text(f"⚠ Error: {e}")
    except BadRequest as et:
        await message.reply_text(f"⚠ Error: {et}")
    except wikipedia.exceptions.DisambiguationError as eet:
        await message.reply_text(
            f"⚠ Error\n There are too many query! Express it more!\nPossible query result:\n{eet}"
        )


@alia.on_message(filters.command("ud"))
async def ud(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.reply_text("Please enter keywords to search!")
        return
    text = args[1].lower()
    try:
        results = await AioHttp().get_json(f"http://api.urbandictionary.com/v0/async define?term={text}")
        reply_text = f'Word: {text}\nasync definition: {results["list"][0]["async definition"]}'
        reply_text += f'\n\nExample: {results["list"][0]["example"]}'
    except IndexError:
        reply_text = (
            f"Word: {text}\nResults: Sorry could not find any matching results!"
        )
    ignore_chars = "[]"
    for chars in ignore_chars:
        reply = reply_text.replace(chars, "")
    if len(reply) >= 4096:
        reply = reply[:4096]  # max msg lenth of tg.
    try:
        await message.reply_text(reply)
    except BadRequest as err:
        await message.reply_text(f"Error! {err.message}")


@alia.on_message(filters.command("wall"))
async def wall(client, message):
    chat_id = message.chat.id
    msg_id = message.message_id
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.reply_text("Please enter a query!")
        return
    query = args[1]
    caption = query
    term = query.replace(" ", "%20")
    json_rep = await AioHttp().get_json(
        f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}"
    )
    if not json_rep.get("success"):
        await message.reply_text("An error occurred!")
        return
    wallpapers = json_rep.get("wallpapers")
    if not wallpapers:
        await message.reply_text("No results found! Refine your search.")
        return
    index = randint(0, len(wallpapers) - 1)  # Choose random index
    wallpaper = wallpapers[index]
    wallpaper = wallpaper.get("url_image")
    wallpaper = wallpaper.replace("\\", "")
    await client.send_photo(
        chat_id,
        photo=wallpaper,
        caption="Preview",
        reply_to_message_id=msg_id,
        timeout=60,
    )
    await client.send_document(
        chat_id,
        document=wallpaper,
        filename="wallpaper",
        caption=caption,
        reply_to_message_id=msg_id,
        timeout=60,
    )


@alia.on_message(filters.command("imdb"))
async def imdb(client, message):
    try:
        args = message.text.split(None, 1)
        movie_name = args[1]
        remove_space = movie_name.split(" ")
        final_name = "+".join(remove_space)
        page = await AioHttp().get(
            "https://www.imdb.com/find?ref_=nv_sr_fn&q=" + final_name + "&s=all"
        )
        soup = BeautifulSoup(page.content, "lxml")
        odds = soup.findAll("tr", "odd")
        mov_title = odds[0].findNext("td").findNext("td").text
        mov_link = (
            "http://www.imdb.com/" + odds[0].findNext("td").findNext("td").a["href"]
        )
        page1 = await AioHttp().get(mov_link)
        soup = BeautifulSoup(page1.content, "lxml")
        if soup.find("div", "poster"):
            poster = soup.find("div", "poster").img["src"]
        else:
            poster = ""
        if soup.find("div", "title_wrapper"):
            pg = soup.find("div", "title_wrapper").findNext("div").text
            mov_details = re.sub(r"\s+", " ", pg)
        else:
            mov_details = ""
        credit = soup.findAll("div", "credit_summary_item")
        director = credit[0].a.text
        if len(credit) == 1:
            writer = "Not available"
            stars = "Not available"
        elif len(credit) > 2:
            writer = credit[1].a.text
            actors = [x.text for x in credit[2].findAll("a")]
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        else:
            writer = "Not available"
            actors = [x.text for x in credit[1].findAll("a")]
            actors.pop()
            stars = actors[0] + "," + actors[1] + "," + actors[2]
        if soup.find("div", "inline canwrap"):
            story_line = soup.find("div", "inline canwrap").findAll("p")[0].text
        else:
            story_line = "Not available"
        info = soup.findAll("div", "txt-block")
        if info:
            mov_country = []
            mov_language = []
            for node in info:
                a = node.findAll("a")
                for i in a:
                    if "country_of_origin" in i["href"]:
                        mov_country.append(i.text)
                    elif "primary_language" in i["href"]:
                        mov_language.append(i.text)
        if soup.findAll("div", "ratingValue"):
            for r in soup.findAll("div", "ratingValue"):
                mov_rating = r.strong["title"]
        else:
            mov_rating = "Not available"
        msg = f"*Title :* {mov_title}\n{mov_details}\n*Rating :* {mov_rating} \n*Country :*  {mov_country}\n*Language :* {mov_language}\n*Director :* {director}\n*Writer :* {writer}\n*Stars :* {stars}\n*IMDB Url :* {mov_link}\n*Story Line :* {story_line}"
        await message.reply_photo(
            photo=poster, caption=msg, parse_mode="markdown"
        )
    except IndexError:
        await message.reply_text("Plox enter **Valid movie name** kthx")


@alia.on_message(filters.command("getlink"))
async def getlink(client, message):
    args = message.text.split(None, 1)
    if len(args) >= 2:
        pattern = re.compile(r"-\d+")
    else:
        await message.reply_text("You don't seem to be referring to any chats.")
    links = "Invite link(s):\n"
    for chat_id in pattern.findall(message.text):
        try:
            chat = await client.get_chat(chat_id)
            bot_member = chat.get_member(bot_id)
            if bot_member.can_invite_users:
                invitelink = await client.export_chat_invite_link(chat_id)
                links += str(chat_id) + ":\n" + invitelink + "\n"
            else:
                links += (
                    str(chat_id) + ":\nI don't have access to the invite link." + "\n"
                )
        except BadRequest as excp:
            links += str(chat_id) + ":\n" + excp.message + "\n"
    await message.reply_text(links)


@alia.on_message(filters.command("rmeme"))
async def rmemes(client, message):
    chat = message.chat
    SUBREDS = [
        "meirl",
        "dankmemes",
        "AdviceAnimals",
        "memes",
        "meme",
        "memes_of_the_dank",
        "PornhubComments",
        "teenagers",
        "memesIRL",
        "insanepeoplefacebook",
        "terriblefacebookmemes",
    ]
    subreddit = random.choice(SUBREDS)
    res = await AioHttp().get_json(f"https://meme-api.herokuapp.com/gimme/{subreddit}")
    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))
    caps = f"× <b>Title</b>: {title}\n"
    caps += f"× <b>Subreddit:</b> <pre>r/{rpage}</pre>"
    keyb = [[InlineKeyboardButton(text="Subreddit Postlink 🔗", url=plink)]]
    try:
        await client.send_photo(
            chat.id,
            photo=memeu,
            caption=(caps),
            reply_markup=InlineKeyboardMarkup(keyb),
            timeout=60,
            parse_mode="HTML",
        )
    except BadRequest as excp:
        return await message.reply_text(f"Error! {excp.message}")


@alia.on_message(filters.user(OWNER_ID) & filters.command("stats"))
async def stats(client, message):
    await message.reply_text(
        "Current stats:\n" + "\n".join(mod.__stats__() for mod in STATS)
    )


__help__ = """
An "odds and ends" module for small, simple commands which don't really fit anywhere

 × /id: Get the current group id. If used by replying to a message, gets that user's id.
 × /info: Get information about a user.
 × /wiki : Search wikipedia articles.
 × /rmeme: Sends random meme scraped from reddit.
 × /ud <query> : Search stuffs in urban dictionary.
 × /wall <query> : Get random wallpapers directly from bot!
 × /gdpr: Deletes your information from the bot's database. Private chats only.
 × /imdb <movie>: search movie info and other stuff
 × /markdownhelp: Quick summary of how markdown works in telegram - can only be called in private chats.
"""

__mod_name__ = "Miscs"
