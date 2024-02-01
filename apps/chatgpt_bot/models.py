from django.db import models
import uuid
from apps.bot_main_setup.models import TelegramProfile, TelegramBot

AVAILABLE_TEXT_MODELS_CHOICES = [
    ("gpt-3.5-turbo", "GPT-3.5 Turbo"),
    ("gpt-3.5-turbo-16k", "GPT-3.5 Turbo 16k"),
    ("gpt-4-1106-preview", "GPT-4 1106 Preview"),
    ("gpt-4", "GPT-4"),
    ("text-davinci-003", "Text Davinci 003"),
]


class TextModel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Text Model"
        verbose_name_plural = "Text Models"
        db_table = "text_model"
        unique_together = ("name", "key")


class Subscribtion(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    n_tokens = models.IntegerField()
    n_images = models.IntegerField()
    n_tts = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subscribtion"
        verbose_name_plural = "Subscribtions"
        db_table = "subscribtion"


class TokenPackage(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.FloatField()
    n_tokens = models.IntegerField()
    n_images = models.IntegerField()
    n_tts = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Token Package"
        verbose_name_plural = "Token Packages"
        db_table = "token_package"


class ChatGptUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(TelegramProfile, on_delete=models.SET_NULL, verbose_name="Telegram User", null=True,
                             blank=True)
    chat_id = models.BigIntegerField(null=True, blank=True)
    last_interaction = models.DateTimeField(auto_now=True)
    first_seen = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    current_chat_mode = models.CharField(max_length=255, default="assistant")
    current_model = models.ForeignKey(TextModel, on_delete=models.SET_NULL, null=True, blank=True)
    n_used_tokens = models.PositiveBigIntegerField(null=True, blank=True)
    n_generated_images = models.IntegerField(default=0, null=True, blank=True)
    n_transcribed_seconds = models.IntegerField(default=0, null=True, blank=True)
    user_allowed = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    user_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.user_token:
            self.user_token = uuid.uuid4()
        super(ChatGptUser, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "ChatGpt User"
        verbose_name_plural = "ChatGpt Users"


class Dialog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(ChatGptUser, on_delete=models.CASCADE, verbose_name="ChatGpt User")
    chat_mode = models.CharField(max_length=255, default="assistant")
    start_time = models.DateTimeField(auto_now_add=True)
    gpt_model = models.ForeignKey(TextModel, on_delete=models.SET_NULL, null=True, blank=True)
    bot = models.ForeignKey(TelegramBot, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dialog"
        verbose_name_plural = "Dialogs"
        db_table = "dialog"


class Messages_dialog(models.Model):
    user = models.TextField()
    bot = models.TextField()
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Messages Dialog"
        verbose_name_plural = "Messages Dialogs"
        db_table = "messages_dialog"


class Chat_mode(models.Model):
    key = models.CharField(max_length=200)
    model_name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=200, null=True, blank=True)
    welcome_message = models.TextField()
    prompt_start = models.TextField(null=True, blank=True)
    parse_mode = models.CharField(max_length=200, null=True, blank=True, default="html")
    extra_field = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = "Chat Mode"
        verbose_name_plural = "Chat Modes"
        db_table = "chat_mode"


class Config(models.Model):
    openai_api_base = models.CharField(null=True, blank=True, max_length=200)
    new_dialog_timeout = models.IntegerField(null=True, blank=True, default=600)
    return_n_generated_images = models.IntegerField(default=1)
    n_chat_modes_per_page = models.IntegerField(default=5)
    image_size = models.CharField(max_length=200, default="512x512")
    enable_message_streaming = models.BooleanField(default=True)
    chatgpt_price_per_1000_tokens = models.FloatField(default=0.006)
    gpt_price_per_1000_tokens = models.FloatField(default=0.002)
    whisper_price_per_1_min = models.FloatField(default=0.006)
    extra_field = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Config"

    class Meta:
        verbose_name = "Config"
        verbose_name_plural = "Configs"


class GptModels(models.Model):
    model = models.CharField(max_length=200, unique=True)
    config = models.JSONField()

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "Gpt Model"
        verbose_name_plural = "Gpt Models"
        db_table = "gpt_models"
