# Generated by Django 5.0.1 on 2024-02-01 19:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatgpt_bot", "0008_alter_dialog_gpt_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dialog",
            name="chat_mode",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="chatgpt_bot.chat_mode"
            ),
        ),
    ]
