from openai import AsyncOpenAI
from zed.model.defs import OpenAIMessage, Settings
from zed.utils.render_utils import render_template

from .defs import CliPromptInput


class Runner:

    def __init__(self, client: AsyncOpenAI):
        self.client = client
        self.template = "template"
        self.settings = Settings(
            model="gpt-3.5-turbo",
            max_tokens=64,
            temperature=0.0,
            stream=False,
        )

    async def run_prompt(self, prompt_input: CliPromptInput) -> str:
        rendered_prompt = render_template(
            origin_path=__file__, template_name=self.template
        )

        messages = [
            OpenAIMessage(
                role="assistant",
                content=rendered_prompt,
            ),
        ]

        print(f"Calling OpenAI with args {self.settings.to_dict()}")
        result = await self.client.chat.completions.create(
            **self.settings.to_dict(),
            messages=messages,
        )

        print(f"OAI {result = }")
        return result.choices[0].message.content
