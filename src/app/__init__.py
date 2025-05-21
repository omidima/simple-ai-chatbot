from src.app.__base import *
from src.app.skills import skills
from src.skills import ConversationSkill


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("memory", [])

    for item in skills:
        item.regeister()

    await cl.context.emitter.set_commands(COMMANDS)


@cl.on_chat_end
def on_chat_end():
    cl.user_session.set("memory", [])

@cl.on_message
async def on_message(message: cl.Message):

    if (message.command == None):
        await ConversationSkill().run(message)

    for item in skills:
        await item.run(message=message)

    message.command = None
    await message.update()