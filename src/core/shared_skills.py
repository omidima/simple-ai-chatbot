from src.app.__base import *

async def generate_response(message: str, prompts: list = []):
    response = await client.chat.completions.create(
        messages=[*prompts, {"content": message, "role": "user"}], **settings
    )

    return response.choices[0].message.content


async def receive_message(message: str, prompts: list = []):
    if cl.user_session.get("message_history") is None:
        cl.user_session.set("message_history", prompts)

    message_history = cl.user_session.get("message_history", [])

    msg = cl.Message(content="")
    message_history.append({"role": "user", "content": message})
    message_history.append({"role": "assistant", "content": msg.content})

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, model="gpt-4o"
    )

    async for part in stream:
        if part != None:
            if token := part.choices[0].delta.content or "":
                await msg.stream_token(token)
                message_history[-1]["content"] = msg.content

    cl.user_session.set("message_history", message_history)

    await msg.update()
