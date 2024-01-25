from django.shortcuts import render

# Create your views here.
from utils.decarators import get_member
from apps.bot.models import TelegramProfile
import logging
from telegram.ext import  CallbackContext
from telegram import  Update


logger = logging.getLogger(__name__)

@get_member
async def start(update: Update, context: CallbackContext, tg_user: TelegramProfile):
    """Send a message asynchronously when the command /start is issued."""


    try:
        await update.message.reply_text("Assalomu alaykum, common bot ishladi")
    except Exception as e:
        logger.error(f"Error in start command: {e}")
