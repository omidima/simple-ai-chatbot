from src.core.base_skill_class import AISkill
from src.core.shared_skills import receive_message

class ConversationSkill(AISkill):
    def __init__(self):
        super().__init__(None, "desc", "icon", False)

    async def run(self, message):
        await receive_message(message=message.content)