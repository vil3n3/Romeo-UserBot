from pyrogram.types import InlineKeyboardButton, WebAppInfo

class Data:

    text_help_menu = (
        "**𝓾丂乇𝓡-​ꪜ𝓲ꪶꪶ𝓲ꪖ​ꪀ**\n**COMMAND PREFIX;-** `.`"
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("'", "")
    )
    reopen = [[InlineKeyboardButton("Re-Open", callback_data="reopen")]]
