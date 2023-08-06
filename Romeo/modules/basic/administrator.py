import os
import sys
from re import sub
from time import time
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message


DEVS = ["1813373023"]
admins_in_chat = {}

from Romeo.modules.help import add_command_help
from Romeo.modules.basic.profile import extract_user

async def extract_user_and_reason(message, sender_chat=False):
    args = message.text.strip().split()
    text = message.text
    user = None
    reason = None
    if message.reply_to_message:
        reply = message.reply_to_message
        if not reply.from_user:
            if (
                reply.sender_chat
                and reply.sender_chat != message.chat.id
                and sender_chat
            ):
                id_ = reply.sender_chat.id
            else:
                return None, None
        else:
            id_ = reply.from_user.id

        if len(args) < 2:
            reason = None
        else:
            reason = text.split(None, 1)[1]
        return id_, reason

    if len(args) == 2:
        user = text.split(None, 1)[1]
        return await extract_userid(message, user), None

    if len(args) > 2:
        user, reason = text.split(None, 2)[1:]
        return await extract_userid(message, user), reason

    return user, reason


async def list_admins(client: Client, chat_id: int):
    global admins_in_chat
    if chat_id in admins_in_chat:
        interval = time() - admins_in_chat[chat_id]["last_updated_at"]
        if interval < 3600:
            return admins_in_chat[chat_id]["data"]

    admins_in_chat[chat_id] = {
        "last_updated_at": time(),
        "data": [
            member.user.id
            async for member in client.get_chat_members(
                chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
            )
        ],
    }
    return admins_in_chat[chat_id]["data"]




unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@Client.on_message(
    filters.group & filters.command(["setchatphoto", "setgpic"], ".") & filters.me
)
async def set_chat_photo(client: Client, message: Message):
    zuzu = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    can_change_admin = zuzu.can_change_info
    can_change_member = message.chat.permissions.can_change_info
    if not (can_change_admin or can_change_member):
        await message.edit_text("You don't have enough permission")
    if message.reply_to_message:
        if message.reply_to_message.photo:
            await client.set_chat_photo(
                message.chat.id, photo=message.reply_to_message.photo.file_id
            )
            return
    else:
        await message.edit_text("Reply to a photo to set it !")



@Client.on_message(filters.group & filters.command("die", ".") & filters.me)
async def member_ban(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("𝑰 𝒅𝒐𝒏'𝒕 𝒉𝒂𝒗𝒆 𝒆𝒏𝒐𝒖𝒈𝒉 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏𝒔")
    if not user_id:
        return await rd.edit("𝑰 𝒄𝒂𝒏'𝒕 𝒇𝒊𝒏𝒅 𝒕𝒉𝒂𝒕 𝒖𝒔𝒆𝒓.")
    if user_id == client.me.id:
        return await rd.edit("𝑰 𝒄𝒂𝒏'𝒕 𝒅𝒊𝒆𝒅 𝒎𝒚𝒔𝒆𝒍𝒇.")
    if user_id in DEVS:
        return await rd.edit("𝑰 𝒄𝒂𝒏'𝒕 𝒅𝒊𝒆 𝒎𝒚 𝒐𝒘𝒏𝒆𝒓!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("𝕀 𝕔𝕒𝕟'𝕥 𝕓𝕒𝕟 𝕒𝕟 𝕒𝕕𝕞𝕚𝕟, 𝕐𝕠𝕦 𝕜𝕟𝕠𝕨 𝕥𝕙𝕖 𝕣𝕦𝕝𝕖𝕤, 𝕤𝕠 𝕕𝕠 𝕚.")
    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    msg = (
        f"**𝕯𝖎𝖊𝖉 𝖀𝖘𝖊𝖗:** {mention}\n"
        f"**🅳🅸🅴🅳 🅱🆈:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"**𝙍𝙚𝙖𝙨𝙤𝙣:** {reason}"
    await message.chat.ban_member(user_id)
    await rd.edit(msg)



@Client.on_message(filters.group & filters.command("alive", ".") & filters.me)
async def member_unban(client: Client, message: Message):
    reply = message.reply_to_message
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("𝑰 𝒅𝒐𝒏'𝒕 𝒉𝒂𝒗𝒆 𝒆𝒏𝒐𝒖𝒈𝒉 𝒑𝒆𝒓𝒎𝒊𝒔𝒔𝒊𝒐𝒏𝒔")
    if reply and reply.sender_chat and reply.sender_chat != message.chat.id:
        return await rd.edit("𝒀𝒐𝒖 𝒄𝒂𝒏𝒏𝒐𝒕 𝒉𝒂𝒗𝒆 𝒆𝒏𝒐𝒖𝒈𝒉 𝒑𝒐𝒘𝒆𝒓 𝒕𝒐 𝒂𝒍𝒊𝒗𝒆𝒅 𝒂 𝒄𝒉𝒂𝒏𝒏𝒆𝒍")

    if len(message.command) == 2:
        user = message.text.split(None, 1)[1]
    elif len(message.command) == 1 and reply:
        user = message.reply_to_message.from_user.id
    else:
        return await rd.edit(
            "𝙋𝙧𝙤𝙫𝙞𝙙𝙚 𝙖 𝙪𝙨𝙚𝙧𝙣𝙖𝙢𝙚 𝙤𝙧 𝙧𝙚𝙥𝙡𝙮 𝙩𝙤 𝙖 𝙪𝙨𝙚𝙧'𝙨 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙩𝙤 𝙖𝙡𝙞𝙫𝙚."
        )
    await message.chat.unban_member(user)
    umention = (await client.get_users(user)).mention
    await rd.edit(f"🅰🅻🅸🆅🅴🅳! {umention}")



@Client.on_message(filters.command(["pin", "unpin"], ".") & filters.me)
async def pin_message(client: Client, message):
    if not message.reply_to_message:
        return await message.edit_text("Reply to a message to pin/unpin it.")
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_pin_messages:
        return await rd.edit("I don't have enough permissions")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await rd.edit(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await rd.edit(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )


@Client.on_message(filters.command("mute", ".") & filters.me)
async def mute(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't mute myself.")
    if user_id in DEVS:
        return await rd.edit("I can't mute my developer!")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("I can't mute an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = (
        f"**Muted User:** {mention}\n"
        f"**Muted By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )
    if reason:
        msg += f"**Reason:** {reason}"
    await message.chat.restrict_member(user_id, permissions=ChatPermissions())
    await rd.edit(msg)



@Client.on_message(filters.group & filters.command("unmute", ".") & filters.me)
async def unmute(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    await message.chat.restrict_member(user_id, permissions=unmute_permissions)
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"Unmuted! {umention}")


@Client.on_message(filters.command(["kick", "dkick"], ".") & filters.me)
async def kick_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message)
    rd = await message.edit_text("`Processing...`")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_restrict_members:
        return await rd.edit("I don't have enough permissions")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't kick myself.")
    if user_id == DEVS:
        return await rd.edit("I can't kick my developer.")
    if user_id in (await list_admins(client, message.chat.id)):
        return await rd.edit("I can't kick an admin, You know the rules, so do i.")
    mention = (await client.get_users(user_id)).mention
    msg = f"""
**Kicked User:** {mention}
**Kicked By:** {message.from_user.mention if message.from_user else 'Anon'}"""
    if message.command[0][0] == "d":
        await message.reply_to_message.delete()
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    try:
        await message.chat.ban_member(user_id)
        await rd.edit(msg)
        await asyncio.sleep(1)
        await message.chat.unban_member(user_id)
    except ChatAdminRequired:
        return await rd.edit("**Maaf Anda Bukan admin**")


@Client.on_message(
    filters.group & filters.command(["promote", "fullpromote"], ".") & filters.me
)
async def promotte(client: Client, message: Message):
    user_id = await extract_user(message)
    umention = (await client.get_users(user_id)).mention
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit("I can't find that user.")
    bot = (await client.get_chat_member(message.chat.id, client.me.id)).privileges
    if not bot.can_promote_members:
        return await rd.edit("I don't have enough permissions")
    if message.command[0][0] == "f":
        await message.chat.promote_member(
            user_id,
            privileges=ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_change_info=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True,
            ),
        )
        return await rd.edit(f"Fully Promoted! {umention}")

    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=True,
            can_delete_messages=True,
            can_manage_video_chats=True,
            can_restrict_members=True,
            can_change_info=True,
            can_invite_users=True,
            can_pin_messages=True,
            can_promote_members=False,
        ),
    )
    await rd.edit(f"Promoted! {umention}")


@Client.on_message(filters.group & filters.command("demote", ".") & filters.me)
async def demote(client: Client, message: Message):
    user_id = await extract_user(message)
    rd = await message.edit_text("`Processing...`")
    if not user_id:
        return await rd.edit("I can't find that user.")
    if user_id == client.me.id:
        return await rd.edit("I can't demote myself.")
    await message.chat.promote_member(
        user_id,
        privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=False,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ),
    )
    umention = (await client.get_users(user_id)).mention
    await rd.edit(f"Demoted! {umention}")


add_command_help(
    "admin",
    [
        ["die [reply/username/userid]", "Ban someone."],
        [
            f"alive [reply/username/userid]",
            "Unban someone.",
        ],
        ["kick [reply/username/userid]", "kick out someone from your group."],
        [
            f"promote `or` .fullpromote",
            "Promote someone.",
        ],
        ["demote", "Demote someone."],
        [
            "mute [reply/username/userid]",
            "Mute someone.",
        ],
        [
            "unmute [reply/username/userid]",
            "Unmute someone.",
        ],
        [
            "pin [reply]",
            "to pin any message.",
        ],
        [
            "unpin [reply]",
            "To unpin any message.",
        ],
        [
            "setgpic [reply ke image]",
            "To set an group profile pic",
        ],
    ],
)
