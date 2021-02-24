
from pyrogram import filters

from alicia import alia, bot_id
from alicia.helpers import (
    user_can_promote,
    user_can_pin,
    user_can_changeinfo,
)
from alicia.utils import mention_html


@alia.on_message(filters.command("promote"))
async def promote(client, message):
    chat = message.chat
    user = message.from_user
    args = message.text.split(None, 1)
    if user_can_promote(client, chat, user) is False:
        message.reply_text("You don't have enough rights to promote someone!")
        return
    elif len(args) >= 2:
        if args[1].isdigit():
            user_mention = int(args[1])
        elif args[1].startswith("@"):
            user_mention = args[1].replace("@", "")
        else:
            await message.reply_text("you mention what?.... 🤷🏻‍♂.")
            return
        member = await client.get_chat_member(chat.id, user_mention)
        user_id = member.user.id
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user
        member = await client.get_chat_member(chat.id, user_id)
    else:
        await message.reply_text("Who i should promote?")
        return
    if member.status in ["administrator", "creator"]:
        await message.reply_text("This person is already an admin...!")
        return
    if user_id == bot_id:
        await message.reply_text("I hope, if i could promote myself!")
        return
    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = await client.get_chat_member(chat.id, bot_id)
    if bot_member.can_promote_members is False:
        await message.reply_text("I'm not admin here, or probably Promote member permission disabled!")
        return
    await client.promote_chat_member(
        chat.id,
        user_id,
        can_change_info=bot_member.can_change_info,
        can_post_messages=bot_member.can_post_messages,
        can_edit_messages=bot_member.can_edit_messages,
        can_delete_messages=bot_member.can_delete_messages,
        can_invite_users=bot_member.can_invite_users,
        can_restrict_members=bot_member.can_restrict_members,
        can_pin_messages=bot_member.can_pin_messages,
    )
    await message.reply_text("Promoted🧡")


@alia.on_message(filters.command("demote"))
async def demote(client, message):
    chat = message.chat
    user = message.from_user
    args = message.text.split(None, 1)
    if user_can_promote(client, chat, user) is False:
        message.reply_text("You don't have enough rights to demote someone!")
        return
    elif len(args) >= 2:
        if args[1].isdigit():
            user_mention = int(args[1])
        elif args[1].startswith("@"):
            user_mention = args[1].replace("@", "")
        else:
            await message.reply_text("you mention what?.... 🤷🏻‍♂.")
            return
        member = await client.get_chat_member(chat.id, user_mention)
        user_id = member.user.id
    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user
        member = await client.get_chat_member(chat.id, user_id)
    else:
        await message.reply_text("Who i should demote?")
        return
    if member.status in "creator":
        await message.reply_text("I'm not gonna demote Creator this group.... 🙄")
        return
    if member.status != "administrator":
        await message.reply_text("How I'm supposed to demote someone who is not even an admin!")
        return
    if user_id == bot_id:
        await message.reply_text("Yeahhh... Not gonna demote myself!")
        return
    # set same perms as bot - bot can't assign higher perms than itself!
    bot_member = await client.get_chat_member(chat.id, bot_id)
    if bot_member.can_promote_members is False:
        await message.reply_text("I'm not admin here, or probably Promote member permission disabled!")
        return
    await client.promote_chat_member(
        chat.id,
        user_id,
        can_change_info=False,
        can_post_messages=False,
        can_edit_messages=False,
        can_delete_messages=False,
        can_invite_users=False,
        can_restrict_members=False,
        can_pin_messages=False,
    )
    await message.reply_text("Successfully demoted!")


@alia.on_message(filters.command("pin"))
async def pin(client, message):
    args = message.reply_text(None, 1)
    user = message.from_user
    chat = message.chat
    if chat.type in ["private", "channel"]:
        await message.reply_text("Nice, Pin on my private chat")
        return
    prev_message = message.reply_to_message
    if user_can_pin(client, chat, user) is False:
        message.reply_text("You are missing rights to pin a message!")
        return
    is_silent = True
    if len(args) >= 2:
        is_silent = not args[1].lower() in ["notify", "loud", "violent"]
    if prev_message:
        try:
            await client.pin_chat_message(
                chat.id, prev_message.message_id, disable_notification=is_silent
            )
        except BaseException as excp:
            await message.reply_text("Error:{}".format(excp))


@alia.on_message(filters.command("unpin"))
async def unpin(client, message):
    chat = message.chat
    user = message.from_user
    args = message.text.split(None, 1)
    if user_can_pin(client, chat, user) is False:
        message.reply_text("You are missing rights to unpin a message!")
        return 
    try:
        if len(args) >= 2:
            if args[1] == "all":
                await client.unpin_all_chat_message(chat.id)
            else:
                pass
        else:
            await client.unpin_chat_message(chat.id)
    except BaseException as excp:
        await message.reply_text("Error:{}".format(excp))


@alia.on_message(filters.command("invite"))
async def invite(client, message):
    user = message.from_user
    chat = message.chat
    args = message.text.split(None, 1)
    member = await client.get_chat_member(chat.id, user.id)
    if member.status != ["creator", "administrator"]:
        await message.reply_text("You're not admin!")
        return
    if chat.type == "private":
        await message.reply_text("This command is meant to use in chat not in PM")
        return
    if chat.username:
        await message.reply_text(chat.username)
    elif chat.type in ["supergroup", "channel"]:
        bot_member = await client.get_chat_member(chat.id, bot_id)
        if bot_member.can_invite_users:
            if len(args) >= 2:
                if args[1].startswith("@"):
                    user_id = args[1].replace("@", "")
                elif args[1].isdigit:
                    user_id = args[1]
                else:
                    await message.reply_text("Seems you're wrong mention user?")
                    return
                await client.add_chat_members(chat.id, user_id)
                await message.reply_text("Successfully invite a user!")
                return
            invitelink = await client.export_chat_invite_link(chat.id)
            await message.reply_text(invitelink)
        else:
            await message.reply_text(
                "I don't have access to the invite link, try changing my permissions!"
            )
    else:
        await message.reply_text(
            "I can only give you invite links for supergroups and channels, sorry!"
        )


@alia.on_message(filters.command("adminlist"))
async def adminlist(client, message):
    chat = message.chat
    administrators = await client.get_chat_members(chat.id, filter="administrators")
    text = "Admins in <b>{}</b>:".format(chat.title or "this chat")
    for admin in administrators:
        user = admin["user"]
        status = admin["status"]
        name = f"{(mention_html(user.id, user.first_name))}"
        if status == "creator":
            text += "\n 🦁 Creator:"
            text += "\n × {} \n\n 🦊 Admin:".format(name)
    for admin in administrators:
        user = admin["user"]
        status = admin["status"]
        name = f"{(mention_html(user.id, user.first_name))}"
        if status == "administrator":
            text += "\n × {}".format(name)
    await message.reply_text(text, parse_mode="HTML")


@alia.on_message(filters.command("settitle"))
async def set_title(client, message):
    args = message.text.split(None, 1)
    chat = message.chat
    user = message.from_user
    member = await client.get_chat_member(chat.id, user.id)
    if member.status != ["creator", "administrator"]:
        await message.reply_text("You're not admin!")
        return
    if message.reply_to_message:
        user_reply = message.reply_to_message.from_user
        user_member = await client.get_chat_member(chat.id, user_reply)
        user_id = user_member.user.id
        if user_member.status == "creator":
            await message.reply_text(
                "This person CREATED the chat, how can i set custom title for him?"
            )
            return
        if user_member.status != "administrator":
            await message.reply_text(
                "Can't set title for non-admins!\nPromote them first to set custom title!"
            )
            return
        if user_id == bot_id:
            await message.reply_text(
                "I can't set my own title myself! Get the one who made me admin to do it for me."
            )
            return
        if len(args) == 1:
            await message.reply_text("Setting blank title doesn't do anything!")
            return
        if len(args[1]) > 16:
            await message.reply_text(
                "The title length is longer than 16 characters.\nTruncating it to 16 characters."
            )
    else:
        await message.reply_text("You don't seem to be referring to a user.")
        return
    try:
        await client.set_administrator_title(chat.id, user_id, args[1])
        await message.reply_text(
            "Sucessfully set title for <b>{}</b> to <code>{}</code>!".format(
                user_member.user.first_name or user_id, args[1][:16]
            ),
            parse_mode="HTML",
        )

    except BaseException as excp:
        await message.reply_text("Error: {}".format(excp))


@alia.on_message(filters.command("setgpic"))
async def setchatpic(client, message):
    chat = message.chat
    user = message.from_user
    if user_can_changeinfo(client, chat, user) is False:
        await message.reply_text("You are missing right to change group info!")
        return
    if message.reply_to_message:
        if message.reply_to_message.photo:
            pic_id = message.reply_to_message.photo.file_id
        elif message.reply_to_message.video:
            pic_id = message.reply_to_message.video.file_id
        elif message.reply_to_message.animation:
            pic_id = message.reply_to_message.animation.file_id
        elif message.reply_to_message.document:
            pic_id = message.reply_to_message.document.file_id
        else:
            await message.reply_text("You can only set some photo and video as chat pic!")
            return
        dlmsg = await message.reply_text("Just a sec...")
        await client.download_media(pic_id, file_name="gpic.png")
        try:
            if message.reply_to_message.video or message.reply_to_message.animation:
                await client.set_chat_photo(chat.id, video=pic_id)
            else:
                await client.set_chat_photo(chat.id, photo=pic_id)
            await dlmsg.edit_text("Successfully set new chatpic!")
        except BaseException as excp:
            await message.reply_text("Error: {}".format(excp))
    else:
        await message.reply_text("Reply to some photo or file to set new chat pic!")


@alia.on_message(filters.command("delgpic"))
async def rmchatpic(client, message):
    chat = message.chat
    user = message.from_user
    if user_can_changeinfo(client, chat, user) is False:
        await message.reply_text("You don't have enough rights to delete group photo")
        return
    try:
        await client.delete_chat_photo(chat.id)
        await message.reply_text("Successfully deleted chat's profile photo!")
    except BaseException as excp:
        await message.reply_text("Error: {}.".format(excp))
        return


@alia.on_message(filters.command("setgtitle"))
async def setchat_title(client, message):
    chat = message.chat
    user = message.from_user
    args = message.text.split(None, 1)
    if user_can_changeinfo(client, chat, user) is False:
        await message.reply_text("You don't have enough rights to change chat info!")
        return
    if len(args) == 1:
        await message.reply_text("Enter some text to set new title in your chat!")
        return
    try:
        await client.set_chat_title(chat.id, args[1])
        await message.reply_text(
            f"Successfully set <b>{args[1]}</b> as new chat title!",
            parse_mode="HTML",
        )
    except BaseException as excp:
        await message.reply_text("Error: {}.".format(excp))
        return


@alia.on_message(filters.command("setdesc"))
async def set_desc(client, message):
    chat = message.chat
    user = message.from_user
    if user_can_changeinfo(client, chat, user) is False:
        await message.reply_text("You're missing rights to change chat info!")
        return
    args = message.text.split(None, 1)
    if len(args) >= 2:
        desc = args[1]
    else:
        await message.reply_text("Setting empty description won't do anything!")
        return
    try:
        if len(desc) > 255:
            await message.reply_text("Description must needs to be under 255 characters!")
            return
        await client.set_chat_description(chat.id, desc)
        await message.reply_text(f"Successfully updated chat description in {chat.title}!")
    except BaseException as excp:
        await message.reply_text("Error: {}".format(excp))


__help__ = """
 × /adminlist: list of admins in the chat

**Admin only:**
 × /pin: Silently pins the message replied to - add `loud`, `notify` or `violent` to give notificaton to users.
 × /unpin: Unpins the currently pinned message.
 × /invite @username[optional]: Gets invitelink or add a user to group chat.
 × /promote: Promotes the user replied to.
 × /demote: Demotes the user replied to.
 × /settitle: Sets a custom title for an admin.
 × /setgpic: As a reply to file or photo to set group profile pic!
 × /delgpic: Same as above but to remove group profile pic.
 × /setgtitle <newtitle>: Sets new chat title in your group.
 × /setdesc: <description> Sets new chat description in group.

**Note**: To set group sticker set chat must needs to have min 100 members.

An example of promoting someone to admins:
`/promote @username`; this promotes a user to admins.
"""

__mod_name__ = "Admin"
