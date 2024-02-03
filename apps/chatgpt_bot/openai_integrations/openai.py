import uuid

import environ
import openai
from asgiref.sync import sync_to_async
from telegram.constants import ParseMode

from apps.chatgpt_bot.models import Dialog, Messages_dialog
from apps.chatgpt_bot.openai_integrations.token_calculator import num_tokens_from_messages

env = environ.Env()
environ.Env.read_env()


@sync_to_async
def create_msg(message, answer, user, input_tokens, output_tokens):
    if Dialog.objects.filter(user=user, end=False).exists():
        dialog = Dialog.objects.filter(user=user, end=False).last()
        dialog.input_tokens += input_tokens
        dialog.output_tokens += output_tokens
        dialog.save()
    else:
        dialog = Dialog.objects.create(
            user=user,
            chat_mode=user.current_chat_mode,
            gpt_model=user.current_model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
    message = Messages_dialog.objects.create(
        user=message,
        bot=answer,
        dialog=dialog,
        msg_token=uuid.uuid4().hex,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )

    return message.msg_token


@sync_to_async
def generate_prompt(user, message,bot_name):
    message=message.replace(f"@{bot_name}","")
    print("message: ", message)

    message=message.strip()

    print("message: ", message)
    message="Qisqa va aniq javob ber:"+message
    promt = user.current_chat_mode.prompt_start
    messages_list = [{"role": "system", "content": promt}]
    if Dialog.objects.filter(user=user, end=False).exists():
        dialog = Dialog.objects.filter(user=user, end=False).last()
        # get last 3 messages
        messages = Messages_dialog.objects.filter(dialog=dialog).order_by("created_at")[:1]
        if messages.count() > 0:
            for msg in messages:
                messages_list.append({"role": "user", "content": msg.user})
                messages_list.append({"role": "assistant", "content": msg.bot})
            messages_list.append({"role": "user", "content": message})
            return messages_list
    else:
        messages_list.append({"role": "user", "content": message})
        return messages_list


async def send_message_stream(message, model_name, chat_token, user, update, context, *args, **kwargs):
    openai.api_key = env.str("OPENAI_API_KEY")

    def _postprocess_answer(answer):
        answer = answer.strip()
        return answer

    answer = None

    messages = await generate_prompt(user, message,context.bot.username)
    print("messages: ", messages)

    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
    msg = await context.bot.send_message(chat_id=update.message.chat_id, text="....", parse_mode=ParseMode.MARKDOWN)

    while answer is None:
        r_gen = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            stream=True,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            timeout=600,
        )
        answer = ""
        i = 1
        for r_item in r_gen:
            delta = r_item.choices[0].delta
            if "content" in delta:
                answer += delta.content
                if len(answer) // 80 == i:
                    msg = await context.bot.edit_message_text(
                        chat_id=update.message.chat_id,
                        text=_postprocess_answer(answer),
                        message_id=msg.message_id,
                        parse_mode=ParseMode.MARKDOWN,
                    )
                    i += 1
        msg = await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            text=_postprocess_answer(answer),
            message_id=msg.message_id,
            parse_mode=ParseMode.MARKDOWN,
        )

        model = user.current_model
        input_message = messages
        output_message = [{"role": "assistant", "content": answer}]

        input_tokens = await num_tokens_from_messages(input_message, model_name)
        output_tokens = await num_tokens_from_messages(output_message, model_name)

        print("input_tokens: ", input_tokens)
        print("output_tokens: ", output_tokens)
        print("user: ", message)
        print("assistant: ", answer)

        await create_msg(message, answer, user, input_tokens, output_tokens)

        return answer
