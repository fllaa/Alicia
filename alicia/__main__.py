import importlib

from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from alicia import LOGGER, OWNER_ID, alia, bot_name, bot_username
from alicia.modules import ALL_MODULES

PM_START_TEXT = f"""
Kon'nichiwa! my name is *{bot_name}*. If you have any questions on how to use me, Click Help button.
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
                                  url=f"t.me/{bot_username}?start=help",)]]


HELP_STRINGS = f"""
Kon'nichiwa! My name is *{bot_name}*.
I'm a advanced modular group management bot with a lot of additional features! \
Have a look at the following for an idea of some of the things I can help you with.
*Main* commands available:
 × /start: Starts me, can be used to check i'm alive or no...
 × /help: PM's you this message.
 × /help <module name>: PM's you info about that module.
 × /settings: in PM: will send you your settings for all supported modules.
   - in a group: will redirect you to pm, with all that chat's settings.
 \nClick on the buttons below to get documentation about specific modules!"""


IMG = "https://telegra.ph/file/3a864035c2f7d46a66a45.mp4"


IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("alicia.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


@alia.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type != "private":
        await message.reply_text("Hi! I am Alive here!")
        return
    try:
        await message.reply_video(IMG, caption=PM_START_TEXT, parse_mode="markdown", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as excp:
        await message.reply_video(f"Error: {excp}")


@alia.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type != "private":
        button = [
            [
                InlineKeyboardButton(
                    text="Help",
                    url="t.me/{}?start=help".format(bot_username))
        ]]
        await message.reply.text("Contact me in PM to get the list of possible commands.", reply_markup=InlineKeyboardMarkup(button))
        return
    try:
        await message.reply_text(HELP_STRINGS, parse_mode="markdown")
    except Exception as excp:
        await message.reply_text(f"Error: {excp}")


if __name__ == "__main__":
    alia.start()
    LOGGER.info("Alicia goes brrrr....!")
    idle()
