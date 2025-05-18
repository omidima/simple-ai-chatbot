import json
import requests
from src.core.shared_skills import generate_response, receive_message
from src.core.base_skill_class import AISkill
from src.core.base_agent import AgentAI, JobItem
from src.app.__base import cl


class TorobSearchAgent(AgentAI):
    def __init__(self, message):
        self.jobs = [
            JobItem(
                **{
                    "title": "آنالیز کردن نیازهای کاربر",
                    "description": "استخراج خواسته کاربر از پیام ارسالی و برگرداندن نام محصولی که میخواهد",
                }
            ),
            JobItem(
                **{"title": "جستجو در ترب", "description": "جستجو کردن محصول در ترب"}
            ),
            JobItem(
                **{
                    "title": "نمایش نتیجه",
                    "description": "نمایش دیتاهای پیدا شده به کاربر",
                }
            ),
        ]
        self.message = message
        super().__init__(self.jobs)

    def create_search_url(self, product_name):
        base_url = f"https://api.torob.com/v4/base-product/search/?page=0&size=24&q={product_name.replace(' ', '-')}&available=true"
        return base_url

    def fetch_search_results(self, search_url):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        return response.json()["results"]

    async def start(self, action):
        await self.init_tasks()

        # Start process tasks
        for index in range(len(self.tasks)):
            self.tasks[index].staus = cl.TaskStatus.RUNNING
            await self.task_list.send()

            if self.jobs[index].title == self.jobs[0].title:
                product_name = await generate_response(
                    f"با توجه به پیام کاربر نام محصولی که میخواهد خریداری کند را استخراج کن و در خروجی برگردان \n {self.message}"
                )
                self.products = self.fetch_search_results(
                    self.create_search_url(product_name)
                )[5]

            if self.jobs[index].title == self.jobs[2].title:
                await receive_message(
                    self.message,
                    [
                        {
                            "role": "user",
                            "content": f"""متناسب با پیام کاربر از لیست محصولات بهترین مورد رو بهش پیشنهاد بده ولینک اون رو ایجاد کن تا بتونه روی اون کلیک کنه، base_url سایت هم https://torob.com هست.

                    سوال کاربر: {self.message}
                    محصولات: {json.dumps(self.products, ensure_ascii=False)}
                    """,
                        }
                    ],
                )

            self.tasks[index].staus = cl.TaskStatus.DONE
            await self.task_list.send()

        self.task_list.status = "Done"
        await self.task_list.send()


class TorobSearchSkill(AISkill):
    def __init__(self):
        super().__init__(
            "حرید از ترب",
            "با استفاده از این ابزارک میتونید از ترب خرید خودتون رو انجام بدید و محصولی که نیاز دارید رو سریع پیدا کنید",
            "mony",
            True,
        )

    async def run(self, message):
        if await super().run(message):
            return

        agent = TorobSearchAgent(message.to_dict()["output"])
        await agent.start(None)
