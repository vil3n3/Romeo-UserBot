import os
import shutil
import asyncio
from git import Repo
from pyrogram.types import Message
from pyrogram import filters, Client
from git.exc import GitCommandError, InvalidGitRepositoryError
from Romeo.helper.basic import edit_or_reply
from Romeo import SUDO_USER

from Romeo.modules.help import *


@Client.on_message(filters.command(["restart", "reload"], ".") & (filters.me | filters.user(SUDO_USER)))
async def restart(client, m: Message):
    reply = await m.edit("**Restarting...**")
    
    await reply.edit(
        "𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙚𝙙 𝙐𝙨𝙚𝙧-𝙑𝙞𝙡𝙡𝙞𝙖𝙣...\n\n💞 𝕎𝕒𝕚𝕥 1-2 𝕞𝕚𝕟𝕦𝕥𝕖𝕤\nLoad plugins...</b>")
    os.system(f"kill -9 {os.getpid()} && python3 -m Romeo")
