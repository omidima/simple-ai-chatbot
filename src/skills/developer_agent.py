from src.core.shared_skills import generate_response, receive_message
from src.core.base_agent import AgentAI,JobItem
from src.core.base_skill_class import AISkill

import json

import logging

log = logging.getLogger("developer agent")

class DevelopingSkill(AISkill):

    def __init__(self):
        log.info("start developing")
        super().__init__("Developer", "Generate applications code", "globe", True)
    
    async def run(self, message):
        if (await super().run(message)):
            return
        
        jobs = await generate_response(
            "",
            [
                {
                    "role": "system",
                    "content": f"""به عنوان یک توسعه دهنده مسئله‌ای رو که کاربر میگه رو بررسی کن و لیستی از کارهایی که باید انجام بده رو به صورت json به من بده تا توی agent استفاده کنم حتما به صورت json باشه و هر آیتم فیلدهای title, description رو داشته باشن.
            نیاز به توضیح نیست و تنها json برگردان

            {message.to_dict()["output"]}
            """,
                }
            ],
        )

        jobs = json.loads(jobs.replace("```json","").replace("```",""))

        agent = AgentAI(
            [JobItem(title=job["title"], description=job["description"]) for job in jobs]
        )

        async def action(j):
            title = j.title
            description = j.description
            await receive_message(
                f"{title} {description}",
                [
                    {
                        "role": "system",
                        "content": "توی یک توسعه‌دهنده و مهندس کامپیوتری هستی، کارهایی که به تو گفته میشه و توضیحاتش رو توسعه بده و به کد تبدیل کن و به من برگردون. زبان توسعه رو خودت انتخاب کن و اصول معماری نرم افزار رو هم رعایت کن.",
                    }
                ],
            )
        await agent.start(action)

        
