from src.app.__base import *


class AISkill:
    def __init__(self, name,desc, icon, is_button= True):
        self.name = name
        self.is_button = is_button
        self.icon = icon
        self.desc = desc

    def regeister(self):
        in_command = None
        for item in COMMANDS:
            if item["id"] == self.name:
                in_command = item

        if in_command is None:
            COMMANDS.append(
                {
                    "id": self.name,
                    "icon": self.icon,
                    "description": self.desc,
                    "button": self.is_button,
                    "persistent": True,
                }
            )

    async def run(self, message: cl.Message):
        if (message.command != self.name):
            return True