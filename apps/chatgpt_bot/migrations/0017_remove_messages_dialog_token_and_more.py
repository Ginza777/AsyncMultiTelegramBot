# Generated by Django 5.0.1 on 2024-02-19 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatgpt_bot', '0016_messages_dialog_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages_dialog',
            name='token',
        ),
        migrations.AlterField(
            model_name='messages_dialog',
            name='bot',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='messages_dialog',
            name='user',
            field=models.TextField(blank=True, null=True),
        ),
    ]