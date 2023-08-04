from Romeo import app
from pyrogram import filters


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
   await message.reply_text("𝐻𝑒𝑦 ꪜ𝓲ꪶꪶ𝓲ꪖꪀ 𝐴𝑠𝑠𝑖𝑠𝑡𝑎𝑛𝑡 𝒉𝑒𝑟𝑒")
