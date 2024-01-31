from channels.db import database_sync_to_async
from apps.chatgpt_bot.models import ChatGptUser, Chat_mode, GptModels
from django.utils.translation import gettext_lazy as _


HELP_MESSAGE = str(_("""Commands:
⚪️ /retry – Regenerate last bot answer
⚪️ /new – Start new dialog
⚪️ /mode – Select chat mode
⚪️ /settings – Show settings
⚪️ /balance – Show balance
⚪️ /help – Show help

🎨 Generate images from text prompts in <b>👩‍🎨 Artist</b> /mode
👥 Add bot to <b>group chat</b>: /help_group_chat
🎤 You can send <b>Voice Messages</b> instead of text
"""))

START_MESSAGE = str(_("Hi! I'm ChatGPT bot 🤖"))

IMPORTANT_MESSAGE = str(_("""Important notes:
1. The longer your dialog, the more tokens are spent with each new message. To start new dialog, send /new command
2. Write in 🇬🇧 English for a better quality of answers
3. GPT-4 Turbo consumes 10x more tokens than ChatGPT. So use it when you really need it"""))


def split_text_into_chunks(text, chunk_size):
    """Split text into chunks of 500 characters."""
    return [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]


@database_sync_to_async
def check_user_exists(tg_user) -> bool:
    return ChatGptUser.objects.filter(user=tg_user).exists()


@database_sync_to_async
def create_user(tg_user) -> object:
    return ChatGptUser.objects.create(user=tg_user, chat_id=tg_user.telegram_id).save()


@database_sync_to_async
def get_user(tg_user) -> object:
    return ChatGptUser.objects.get(user=tg_user)


@database_sync_to_async
def get_user_by_id(telegram_id: int) -> object:
    return ChatGptUser.objects.get(user__telegram_id=telegram_id)


async def save_user_async(user):
    await database_sync_to_async(user.save)()


@database_sync_to_async
def get_chat_mode_name(user_id):
    user = ChatGptUser.objects.get(user__telegram_id=user_id)
    model = user.current_chat_mode
    chat_mode_instance = Chat_mode.objects.get(key=model)
    return chat_mode_instance.model_name

@database_sync_to_async
def models():
    return GptModels.objects.all()


@database_sync_to_async
def get_chat_mode(chat_mode):
    msg=Chat_mode.objects.get(key=chat_mode)
    print(msg)
    return msg.welcome_message
