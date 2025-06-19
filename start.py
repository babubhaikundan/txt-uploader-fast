import asyncio
from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputMediaPhoto,
)
from bot.config import Config, Script
from bot.utils import add_user
from bot.utils.helpers import get_random_thumb, get_random_emoji
from database import db





async def subscribe(app, message):
    if FORCE_SUB:
        try:
          user = await app.get_chat_member(FORCE_SUB, message.from_user.id)
          if str(user.status) == "ChatMemberStatus.BANNED":
              await message.reply_text("You are Banned. Contact -- 𝕂𝕦𝕟𝕕𝕒𝕟 𝕐𝕒𝕕𝕒𝕧 😎")
              return 1
        except UserNotParticipant:
            link = await app.export_chat_invite_link(FORCE_SUB)
            caption = f"Join our channel to use the bot"
            await message.reply_photo(photo="https://instagram.fpat3-1.fna.fbcdn.net/v/t51.2885-19/315573601_166117896103233_5064134256297899561_n.jpg?_nc_ht=instagram.fpat3-1.fna.fbcdn.net&_nc_cat=109&_nc_oc=Q6cZ2QHp1p2fpx5ML7BW36qN418cdMnUuGXOe_EUVZDilIm-ZFpiWPsFQB6GHlKoJbipij76zD-_ZNUpNPH5XSn65M_6&_nc_ohc=BVitlw1kl00Q7kNvwGYBd6N&_nc_gid=Rx4aIkcaOnz6lQwh6XcVdQ&edm=APoiHPcBAAAA&ccb=7-5&oh=00_AfKVu2qFclOBBa2g3ls1_ys0Kwq_bH9Ox_fYdGifPoRYEg&oe=68392B00&_nc_sid=22de04",caption=caption, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Now...", url=f"https://t.me/checkkyadav")]]))
            return 1
        except Exception as ggn:
            await message.reply_text(f"Something Went Wrong. Contact admins... with following message {ggn}")
            return 1 




@Client.on_message(filters.command("start") & filters.private & filters.incoming)
@Client.on_callback_query(filters.regex(r"^start$"))
async def start(bot: Client, message: Message | CallbackQuery):
    func = (
        message.reply_text
        if isinstance(message, Message)
        else message.edit_message_text
    )
    if isinstance(message, Message):
        delete_sts = True
        func = message.reply_text
    else:
        func = message.edit_message_text
        delete_sts = False

    sts = await func(get_random_emoji())

    await asyncio.sleep(1)

    settings_markup = [
        [
            ("ℂ𝔸ℙ𝕋𝕀𝕆ℕ", "custom_caption"),
            ("𝕋ℍ𝕌𝕄𝔹ℕ𝔸𝕀𝕃", "thumbnail"),
        ],
        [
            ("𝕄𝕆𝔻𝔼", "mode"),
            ("ℚ𝕌𝔸𝕃𝕀𝕋𝕐", "quality"),
        ],
        [("ℂℍ𝔸ℕℕ𝔼𝕃", "log_channel")],
    ]

    markup = []

    for row in settings_markup:
        button_row = []
        for button in row:
            button_row.append(InlineKeyboardButton(button[0], callback_data=button[1]))
        markup.append(button_row)

    markup = InlineKeyboardMarkup(markup)
    new_user = await add_user(message.from_user.id)

    if new_user:
        await bot.send_message(
            chat_id=Config.LOG_CHANNEL,
            text=Script.NEW_USER_MESSAGE.format(
                user_id=message.from_user.id,
                mention=message.from_user.mention,
            ),
        )

    data = {"mp4": "Video", "mkv": "Document"}

    text = "\n\nSettings:\n"
    user = await db.users.get_user(message.from_user.id)
    text += f"⪼ Custom Caption: {'✅' if user['custom_caption_enabled'] and user['custom_caption'] else '❌'}\n"
    text += f"⪼ Thumbnail: {'✅' if user['thumbnail_enabled'] and user['thumbnail'] else '❌'}\n"
    text += f"⪼ Mode: {data[user['ext']]}\n"
    text += f"⪼ Quality: {['High', 'Medium', 'Low'][int(user['quality']) - 1]}\n"
    text += f"⪼ Log Channel: {user['log_channel'] or 'Not Set'}"

    kwargs = {
        "text": Script.START_MESSAGE.format(mention=message.from_user.mention) + text,
        "reply_markup": markup,
    }

    if thumb := get_random_thumb():
        if isinstance(message, Message):
            func = message.reply_photo
            kwargs["photo"] = thumb
            kwargs["caption"] = kwargs["text"]
            kwargs.pop("text")
        elif isinstance(message, CallbackQuery):
            if message.message.photo:
                kwargs["media"] = InputMediaPhoto(thumb, caption=kwargs["text"])
                kwargs.pop("text")
                func = message.edit_message_media
                delete_sts = False
            else:
                kwargs["photo"] = thumb
                func = message.message.reply_photo
                kwargs["caption"] = kwargs["text"]
                kwargs.pop("text")

    await func(**kwargs)
    if delete_sts:
        await sts.delete()
