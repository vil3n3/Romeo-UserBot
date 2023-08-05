import asyncio
from datetime import datetime

import humanize
from pyrogram import filters, Client
from pyrogram.types import Message

from Romeo.helper.PyroHelpers import GetChatID, ReplyCheck
from Romeo.modules.help import add_command_help

AFK = False
AFK_REASON = ""
AFK_TIME = ""
USERS = {}
GROUPS = {}


def subtract_time(start, end):
    subtracted = humanize.naturaltime(start - end)
    return str(subtracted)


@Client.on_message(
    ((filters.group & filters.mentioned) | filters.private) & ~filters.me & ~filters.service, group=3
)
async def collect_afk_messages(bot: Client, message: Message):
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME)
        is_group = True if message.chat.type in ["supergroup", "group"] else False
        CHAT_TYPE = GROUPS if is_group else USERS

        if GetChatID(message) not in CHAT_TYPE:
            text = (
                f"`ᴮᵉᵉᵖ ᵇᵒᵒᵖ. ᵀʰⁱˢ ⁱˢ ᵃⁿ ᵃᵘᵗᵒᵐᵃᵗᵉᵈ ᵐᵉˢˢᵃᵍᵉ.\n"
                f"ɪ ᴀᴍ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ʀɪɢʜᴛ ɴᴏᴡ.\n"
                f"𝑳𝒂𝒔𝒕 𝒔𝒆𝒆𝒏: {last_seen}\n"
                f"🆁🅴🅰🆂🅾🅽: ```{AFK_REASON.upper()}```\n"
                f"ˢᵉᵉ ʸᵒᵘ ᵃᶠᵗᵉʳ ᴵ'ᵐ ᵈᵒⁿᵉ ᵈᵒⁱⁿᵍ ʷʰᵃᵗᵉᵛᵉʳ ᴵ'ᵐ ᵈᵒⁱⁿᵍ.`"
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )
            CHAT_TYPE[GetChatID(message)] = 1
            return
        elif GetChatID(message) in CHAT_TYPE:
            if CHAT_TYPE[GetChatID(message)] == 50:
                text = (
                    f"`ᵀʰⁱˢ ⁱˢ ᵃⁿ ᵃᵘᵗᵒᵐᵃᵗᵉᵈ ᵐᵉˢˢᵃᵍᵉ.\n"
                    f"🅻🅰🆂🆃 🆂🅴🅴🅽: {last_seen}\n"
                    f"𝑻𝒉𝒊𝒔 𝒊𝒔 𝒕𝒉𝒆 10𝒕𝒉 𝒕𝒊𝒎𝒆 𝑰'𝒗𝒆 𝒕𝒐𝒍𝒅 𝒚𝒐𝒖 𝑰'𝒎 𝑨𝑭𝑲 𝒓𝒊𝒈𝒉𝒕 𝒏𝒐𝒘..\n"
                    f"𝙸'𝚕𝚕 𝚐𝚎𝚝 𝚝𝚘 𝚢𝚘𝚞 𝚠𝚑𝚎𝚗 𝙸 𝚐𝚎𝚝 𝚝𝚘 𝚢𝚘𝚞.\n"
                    f"𝑁𝑜 𝑚𝑜𝑟𝑒 𝑓𝑜𝑟 𝑦𝑜𝑢 𝑎𝑢𝑡𝑜𝑚𝑎𝑡𝑒𝑑 𝑚𝑒𝑠𝑠𝑎𝑔𝑒.:"
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                )
            elif CHAT_TYPE[GetChatID(message)] > 50:
                return
            elif CHAT_TYPE[GetChatID(message)] % 5 == 0:
                text = (
                    f"`𝐻𝑒𝑦 𝐼'𝑚 𝑠𝑡𝑖𝑙𝑙 𝑛𝑜𝑡 𝑏𝑎𝑐𝑘 𝑦𝑒𝑡.\n"
                    f"🅻🅰🆂🆃 🆂🅴🅴🅽: {last_seen}\n"
                    f"🅂🅃🄸🄻🄻 🄱🅄🅂🅈 : ```{AFK_REASON.upper()}```\n"
                    f"ᵀᴿᵞ ᴾᴵᴺᴳᴵᴺᴳ ᴬ ᴮᴵᵀ ᴸᴬᵀᴱᴿ.`"
                )
                await bot.send_message(
                    chat_id=GetChatID(message),
                    text=text,
                    reply_to_message_id=ReplyCheck(message),
                )

        CHAT_TYPE[GetChatID(message)] += 1


@Client.on_message(filters.command("afk", ".") & filters.me, group=3)
async def afk_set(bot: Client, message: Message):
    global AFK_REASON, AFK, AFK_TIME

    cmd = message.command
    afk_text = ""

    if len(cmd) > 1:
        afk_text = " ".join(cmd[1:])

    if isinstance(afk_text, str):
        AFK_REASON = afk_text

    AFK = True
    AFK_TIME = datetime.now()

    await message.delete()


@Client.on_message(filters.command("afk", "!") & filters.me, group=3)
async def afk_unset(bot: Client, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        await message.edit(
            f"`While you were away (for {last_seen}), you received {sum(USERS.values()) + sum(GROUPS.values())} "
            f"messages from {len(USERS) + len(GROUPS)} chats`"
        )
        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS = {}
        GROUPS = {}
        await asyncio.sleep(5)

    await message.delete()

if AFK:
   @Client.on_message(filters.me, group=3)
   async def auto_afk_unset(bot: Client, message: Message):
       global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

       if AFK:
           last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
           reply = await message.reply(
               f"`While you were away (for {last_seen}), you received {sum(USERS.values()) + sum(GROUPS.values())} "
               f"messages from {len(USERS) + len(GROUPS)} chats`"
           )
           AFK = False
           AFK_TIME = ""
           AFK_REASON = ""
           USERS = {}
           GROUPS = {}
           await asyncio.sleep(5)
           await reply.delete()


add_command_help(
    "afk",
    [
        [".afk", "Activates AFK mode with reason as anything after .afk\nUsage: ```.afk <reason>```"],
        ["!afk", "Deactivates AFK mode."],
    ],
)
