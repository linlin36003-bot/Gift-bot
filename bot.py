import os
import re

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CopyTextButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# python-telegram-bot==22.8
# (pip install python-telegram-bot==22.8)

# ===== Bot Info =====
BOT_ID = 6157455819
BOT_USERNAME = "@Character_Catcher_Bot"

# ===== Bot Token =====
TOKEN = os.getenv("BOT_TOKEN", "").strip()


def find_id(text):
    if not text:
        return None

    match = re.search(
        r"(?m)^\s*(\d+)\s*:",
        text
    )

    if match:
        return match.group(1)

    return None


def find_owner(text):
    if not text:
        return None

    match = re.search(r"@([A-Za-z0-9_]{5,32})", text)
    if match:
        return f"@{match.group(1)}"

    return None


def build_owner_line(owner):
    if owner:
        return (
            f"🧃OᴡO! ᴄʜᴇᴄᴋ ᴏᴜᴛ {owner} sᴀɴ ᴄʜᴀʀᴀᴄᴛᴇʀ!"
        )
    return None


async def send_gift_reply(message, source_text):
    """ID ရှာပြီး .cgift reply ပို့မယ်"""
    character_id = find_id(source_text)

    if not character_id:
        await message.reply_text(
            "❌ ID မတွေ့ပါဘူး။\n\n"
            "ဥပမာ:\n"
            "65: Character Name"
        )
        return

    gift_code = f".cgift {character_id}"

    owner = find_owner(source_text)
    owner_line = build_owner_line(owner)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 Copy",
                copy_text=CopyTextButton(
                    text=gift_code
                )
            )
        ]
    ])

    reply_text = f"🆔 ID: {character_id}\n\n"

    if owner_line:
        reply_text += f"{owner_line}\n\n"

    reply_text += f"<code>{gift_code}</code>"

    await message.reply_text(
        reply_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = update.effective_message

    if not message:
        return

    text = message.text or message.caption

    if not text:
        return

    bot_username = context.bot.username

    is_private = message.chat.type == "private"

    bot_mentioned = (
        f"@{bot_username}".lower() in text.lower()
    )

    is_reply_to_bot = (
        message.reply_to_message is not None
        and message.reply_to_message.from_user is not None
        and message.reply_to_message.from_user.username
        and message.reply_to_message.from_user.username.lower() == bot_username.lower()
    )

    # ===== /g command စစ်ဆေးချက် =====
    # /g ပို့ပြီး reply လုပ်ထားရင် → reply လုပ်ထားတဲ့ message ထဲက ID ကို ရှာမယ်
    g_command = re.match(r"^/g(?:@\w+)?\s*$", text.strip(), flags=re.IGNORECASE)

    if g_command:
        if message.reply_to_message is None:
            await message.reply_text(
                "❌ /g ကို ကဒ် message ကို reply လုပ်ပြီး ပို့ပါ။\n\n"
                "📝 ဥပမာ:\n"
                "ကဒ် message ကို reply လုပ်ပြီး /g ပို့ပါ။"
            )
            return

        # Reply လုပ်ထားတဲ့ message ထဲက စာသားကို ယူမယ်
        source_message = message.reply_to_message
        source_text = source_message.text or source_message.caption

        if not source_text:
            await message.reply_text(
                "❌ Reply လုပ်ထားတဲ့ message ထဲမှာ စာသား မတွေ့ပါဘူး။"
            )
            return

        await send_gift_reply(message, source_text)
        return

    # ===== ပုံမှန် message ဖတ်ခြင်း (mention/reply) =====
    if not is_private and not bot_mentioned and not is_reply_to_bot:
        return

    clean_text = re.sub(
        rf"@{re.escape(bot_username)}",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()

    character_id = find_id(clean_text)

    if not character_id:
        if is_private or bot_mentioned or is_reply_to_bot:
            await message.reply_text(
                "❌ ID မတွေ့ပါဘူး။\n\n"
                "ဥပမာ:\n"
                "65: Character Name"
            )
        return

    gift_code = f".cgift {character_id}"

    owner = find_owner(text)
    owner_line = build_owner_line(owner)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📋 Copy",
                copy_text=CopyTextButton(
                    text=gift_code
                )
            )
        ]
    ])

    reply_text = f"🆔 ID: {character_id}\n\n"

    if owner_line:
        reply_text += f"{owner_line}\n\n"

    reply_text += f"<code>{gift_code}</code>"

    await message.reply_text(
        reply_text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        f"🤖 Card Gift Bot\n"
        f"🆔 Bot ID: {BOT_ID}\n"
        f"👤 Username: {BOT_USERNAME}\n\n"
        "Character message ကို ဒီ Bot ထဲ ပို့ပါ။\n\n"
        "Bot က ID ကိုရှာပြီး\n"
        ".cgift ID အဖြစ် Copy လုပ်လို့ရအောင် ပြပေးပါမယ်။\n\n"
        f"💡 Group ထဲမှာ {BOT_USERNAME} ကို mention လုပ်ပါ။\n"
        f"💡 ဒါမှမဟုတ် ကဒ် message ကို reply လုပ်ပြီး /g ပို့ပါ။"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "📖 အသုံးပြုနည်း\n\n"
        "🔹 နည်းလမ်း ၁:\n"
        "Character message ကို ဒီ Bot ဆီ ပို့ပါ\n"
        "→ Bot က ID ကို ရှာပေးပါမယ်\n\n"
        "🔹 နည်းလမ်း ၂ (/g):\n"
        "ကဒ် message ကို reply လုပ်ပြီး /g ပို့ပါ\n"
        "→ Bot က .cgift ID ကို ချပေးပါမယ်\n\n"
        "📝 ဥပမာ:\n"
        "<code>65: Ayanokoji Kiyotaka</code>\n\n"
        f"💡 Group ထဲမှာ {BOT_USERNAME} ကို mention လုပ်ပါ\n"
        f"💡 ဒါမှမဟုတ် ကဒ် message ကို reply လုပ်ပြီး /g ပို့ပါ။",
        parse_mode="HTML"
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN မသတ်မှတ်ထားပါ။"
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.CAPTION,
            handle_message
        )
    )

    print(f"Bot running...")
    print(f"Bot ID: {BOT_ID}")
    print(f"Username: {BOT_USERNAME}")

    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
