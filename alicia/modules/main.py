from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from alicia import OWNER_ID, alia, bot_name, bot_username

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


@alia.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type != "private":
        await message.reply_text("Hi! I am Alive here!")
        return
    try:
        await message.reply_video(IMG, caption=PM_START_TEXT, parse_mode="markdown", reply_markup=InlineKeyboardMarkup(buttons))
    except Exception as excp:
        await message.reply_text(f"Error: {excp}")


@alia.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type != "private":
        button = [
            [
                InlineKeyboardButton(
                    text="Help",
                    url="t.me/{}?start=help".format(bot_username))
        ]]
        await message.reply_text("Contact me in PM to get the list of possible commands.", reply_markup=InlineKeyboardMarkup(button))
        return
    try:
        await message.reply_text(HELP_STRINGS, parse_mode="markdown")
    except Exception as excp:
        await message.reply_text(f"Error: {excp}")

