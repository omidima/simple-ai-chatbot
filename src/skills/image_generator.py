from src.core.shared_skills import generate_response
from src.core.base_skill_class import AISkill
from g4f import Client
import requests

from src.app.__base import cl

import logging

log = logging.getLogger("image maker agent")

class ImageGeneratorSkill(AISkill):
    def __init__(self):
        log.info("start image maker")
        super().__init__("Image Maker", "Make the image of your idea", "image", True)

    async def run(self, message):
        if (await super().run(message)):
            return
        
        client = Client()

        text = message.to_dict()["output"]

        text = await generate_response(
            f"این متن رو به انگلیسی ترجمه کن و بهم بده. \n {text}"
        )
        response = await client.images.generate(model="flux", prompt=text, response_format="url")

        path = f"./media/{response.data[0].url.split('/')[-1]}"
        open(path, "wb").write(requests.get(response.data[0].url).content)
        image = cl.Image(
            path=path, name=response.data[0].url.split("/")[-1], display="inline"
        )

        
        await cl.Message(
            "حواست باشه توی این مدل من حافظه ندارم و نمیتونم تصاویری که تولید کردم رو دوباره ویرایش کنم. پس دوباره کامل باید همه رو برام توضیح بدی.",
            elements=[image],
            command=None
        ).send()