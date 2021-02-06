import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from __main__ import HELPABLE  # pylint: disable-msg=E0611
from alicia import IMG, OWNER_ID, alia, bot_name, bot_username
from alicia.helpers import paginate_modules

PM_START_TEXT = f"""
Hi! my name is **{bot_name}**. If you have any questions on how to use me, Click Help button.
I'm here to make your group management fun and easy!
i have lots of handy features, such as flood control, a warning system, a note keeping system, and even replies on predetermined filters.
Thanks to [my creator](tg://user?id={OWNER_ID}).
Wanna Add me to your Group? Just click the button below!
"""

buttons = [
    [
        InlineKeyboardButton(
            text="Add to Group 👥",
            url="t.me/{bot_username}?startgroup=true"),
        InlineKeyboardButton(
            text="Join Channel ℹ️",
            url="https://t.me/fvllprojekt"),
    ]]

buttons += [[InlineKeyboardButton(text="Help & Commands ❔",
                                  callback_data="help_back")]]

HELP_STRINGS = f"""
Hi! My name is **{bot_name}**.
I'm a advanced modular group management bot with a lot of additional features! \
Have a look at the following for an idea of some of the things I can help you with.
**Main** commands available:
 × /start: Starts me, can be used to check i'm alive or no...
 × /help: PM's you this message.
 × /help <module name>: PM's you info about that module.
 × /settings: in PM: will send you your settings for all supported modules.
   - in a group: will redirect you to pm, with all that chat's settings.
 \nClick on the buttons below to get documentation about specific modules!"""


async def help_button_callback(_, __, query):
    if re.match(r"help_", query.data):
        return True


async def start_callback(_, __, query):
    if re.match(r"bot_start", query.data):
        return True


help_button_create = filters.create(help_button_callback)
start_callback_create = filters.create(start_callback)


@alia.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type != "private":
        await message.reply_text("Hi! I am Alive here!")
        return
    await message.reply_photo(IMG, caption=PM_START_TEXT, parse_mode="markdown", reply_markup=InlineKeyboardMarkup(buttons))


@alia.on_callback_query(start_callback_create)
async def send_start(client, query):
    await query.message.edit(text=PM_START_TEXT, parse_mode="markdown", reply_markup=InlineKeyboardMarkup(buttons))


async def send_help(client, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    await client.send_photo(
        chat_id=chat_id,
        photo=IMG,
        caption=text,
        parse_mode="markdown",
        reply_markup=keyboard)


@alia.on_callback_query(help_button_create)
async def help_button(client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    if mod_match:
        module = mod_match.group(1)
        text = (
            "Here is the help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        await query.message.edit(
            text=text,
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="⬅️ Back", callback_data="help_back")]]
            ),
        )
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=HELP_STRINGS,
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
        )
    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=HELP_STRINGS,
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
        )
    elif back_match:
        await query.message.edit_text(
            text=HELP_STRINGS,
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
        )

@alia.on_message(filters.command("help"))
async def help(client, message):
    chat = message.chat
    args = message.text.split(None, 1)
    if chat.type != "private":
        button = [
            [
                InlineKeyboardButton(
                    text="Help",
                    url="t.me/{}?start=help".format(bot_username))
        ]]
        await message.reply_text("Contact me in PM to get the list of possible commands.", reply_markup=InlineKeyboardMarkup(button))
        return
    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):

        module = args[1].lower()

        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        await send_help(
            client,
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )
    else:
        await send_help(
            client,
            chat.id,
            HELP_STRINGS
        )

